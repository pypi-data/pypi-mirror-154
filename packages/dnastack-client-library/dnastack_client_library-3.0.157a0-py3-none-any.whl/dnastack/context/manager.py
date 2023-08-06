from json import JSONDecodeError

import re
import requests
import yaml
from imagination.decorator import service
from typing import Optional, List, Iterator, Iterable
from urllib.parse import urljoin, urlparse

from dnastack.auth.manager import AuthManager
from dnastack.client.factory import EndpointRepository
from dnastack.client.service_registry.client import ServiceRegistry, STANDARD_SERVICE_REGISTRY_TYPE_V1_0
from dnastack.client.service_registry.factory import ClientFactory, UsePreConditionError
from dnastack.client.service_registry.manager import ServiceRegistryManager
from dnastack.common.events import EventSource
from dnastack.common.logger import get_logger
from dnastack.configuration.manager import ConfigurationManager
from dnastack.configuration.models import ServiceEndpoint, Context, Configuration, ContextSource


@service.registered()
class ContextManager:
    _re_http_scheme = re.compile(r'^https?://')
    _logger = get_logger('ContextManager')

    def __init__(self, config_manager: ConfigurationManager):
        self._config_manager = config_manager
        self.__events = EventSource(['context-sync', 'auth-begin', 'auth-disabled', 'auth-end'])

    @property
    def events(self):
        return self.__events

    def use(self,
            hostname: str,
            no_auth: Optional[bool] = False,
            config_repo_url: str = 'https://dnastack.github.io/dnastack-client-configuration',
            in_isolation: bool = False) -> EndpointRepository:
        """
        Import a configuration from host's service registry (if available) or the corresponding public configuration
        from cloud storage. If "no_auth" is not set to True, it will automatically initiate all authentication.

        The "in_isolation" argument is to prevent the current configuration from being overridden. It is designed to
        use in the library mode. When it is set to "true", instead of loading the configuration from the configuration
        file, this method will use a dummy/blank configuration object.
        """
        base_url = hostname if self._re_http_scheme.search(hostname) else f'https://{hostname}'
        context_name = urlparse(base_url).netloc

        context_logger = get_logger(f'{self._logger.name}/{context_name}')

        config = self._config_manager.load() if not in_isolation else Configuration()
        context = config.contexts.get(context_name)
        is_new_context = context is None
        if is_new_context:
            context = config.contexts[context_name] = Context(
                source=ContextSource(
                    uri=f'{config_repo_url}{"" if config_repo_url.endswith("/") else "/"}{context_name}.yml'
                )
            )

        # Instantiate the service registry manager for the upcoming sync operation.
        reg_manager = ServiceRegistryManager(config, context_name, in_isolation)
        reg_manager.events.on('endpoint-sync', lambda e: self.events.dispatch('context-sync', e))

        active_registries: List[ServiceEndpoint] = []

        # Trigger sync operation
        if is_new_context:
            registry = self.registry(context_name)
            if registry:
                reg_manager.add_registry_and_import_endpoints(registry.endpoint.id,
                                                              registry.endpoint.url)
                active_registries.append(registry.endpoint)
            elif context.source:
                # Look up for a public context config in case that the scanning fails
                # and replace the target context with the imported one.
                response = requests.get(context.source.uri)
                config.contexts[context_name] = Context(**yaml.load(response.text, Loader=yaml.SafeLoader))
            else:
                raise RuntimeError(f'Failed to initiate a new context, called {context_name}, as the code cannot '
                                   'find the service registry endpoint')
        else:
            active_registries.extend(self._get_service_registry_endpoints_from(config, context_name))
            for reg_endpoint in active_registries:
                reg_manager.synchronize_endpoints(reg_endpoint.id)

        # Set the current context.
        config.current_context = context_name

        # Save it to the configuration file.
        if not in_isolation:
            self._config_manager.save(config)

        # Initiate the authentication procedure.
        if no_auth:
            self.events.dispatch('auth-disabled', dict())
        else:
            auth_manager = AuthManager(config)

            # Set up an event relay.
            self.events.relay_from(auth_manager.events, 'auth-begin')
            self.events.relay_from(auth_manager.events, 'auth-end')

            auth_manager.initiate_authentications()

        # Then, return the repository.
        return EndpointRepository(config.contexts[context_name].endpoints,
                                  cacheable=True,
                                  updater=RepositoryUpdater(reg_manager, active_registries))

    def _get_service_registry_endpoints_from(self, config: Configuration, context_name: str) -> List[ServiceEndpoint]:
        return [
            endpoint
            for endpoint in config.contexts[context_name].endpoints
            if endpoint.type == STANDARD_SERVICE_REGISTRY_TYPE_V1_0
        ]

    @classmethod
    def registry(cls, hostname: str) -> Optional[ServiceRegistry]:
        # Scan the service for the list of service info.
        base_url = hostname if cls._re_http_scheme.search(hostname) else f'https://{hostname}'
        context_name = urlparse(base_url).netloc

        target_registry_url: Optional[str] = None

        # Base-registry-URL-to-listing-URL map
        potential_registry_base_paths = [
            # This is for a service which implements the service registry at root.
            '/',

            # This is for a collection service.
            '/service-registry/',

            # This is for an explorer service, e.g., viral.ai.
            '/api/service-registry/',
        ]

        for api_path in potential_registry_base_paths:
            registry_url = urljoin(base_url, api_path)
            listing_url = urljoin(registry_url, 'services')

            try:
                response = requests.get(listing_url, headers={'Accept': 'application/json'})
            except requests.exceptions.ConnectionError:
                continue

            if response.ok:
                try:
                    ids = sorted([entry['id'] for entry in response.json()])
                    cls._logger.debug(f'CHECK: IDS => {", ".join(ids)}')
                except JSONDecodeError:
                    # Look for the next one.
                    continue

                target_registry_url = registry_url

                break
            # end: if

        if target_registry_url:
            return ServiceRegistry.make(ServiceEndpoint(id=context_name, url=target_registry_url))
        else:
            return None


class RepositoryUpdater:
    def __init__(self, reg_manager: ServiceRegistryManager, active_registries: List[ServiceEndpoint]):
        self.__reg_manager = reg_manager
        self.__active_registries = active_registries

    def __call__(self) -> Iterable[ServiceEndpoint]:
        return self.perform_update(self.__reg_manager, self.__active_registries)

    @classmethod
    def perform_update(cls,
                       reg_manager: ServiceRegistryManager,
                       active_registries: List[ServiceEndpoint]) -> Iterable[ServiceEndpoint]:
        for reg_endpoint in active_registries:
            reg_manager.synchronize_endpoints(reg_endpoint.id)
        return reg_manager.get_endpoint_iterator()