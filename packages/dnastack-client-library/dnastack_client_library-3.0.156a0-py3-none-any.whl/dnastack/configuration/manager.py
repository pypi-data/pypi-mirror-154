import os
import shutil
import yaml
from imagination.decorator import service, EnvironmentVariable

from dnastack.common.logger import get_logger
from dnastack.configuration.models import Configuration
from dnastack.configuration.wrapper import ConfigurationWrapper
from dnastack.constants import CLI_DIRECTORY


@service.registered(
    params=[
        EnvironmentVariable('DNASTACK_CONFIG_FILE', default=os.path.join(CLI_DIRECTORY, 'config.yaml'),
                            allow_default=True)
    ]
)
class ConfigurationManager:
    def __init__(self, file_path: str):
        self.__logger = get_logger(f'{type(self).__name__}')
        self.__file_path = file_path
        self.__swap_file_path = f'{self.__file_path}.swp'

    def load_raw(self) -> str:
        """ Load the raw configuration content """
        if not os.path.exists(self.__file_path):
            return '{}'
        with open(self.__file_path, 'r') as f:
            return f.read()

    def load(self) -> Configuration:
        """ Load the configuration object """
        raw_config = self.load_raw()
        if not raw_config:
            return Configuration()
        config = Configuration(**yaml.load(raw_config, Loader=yaml.SafeLoader))
        return ConfigurationWrapper.migrate(config)

    def save(self, configuration: Configuration):
        """ Save the configuration object """
        # Note (1): This is designed to have file operation done as quickly as possible to reduce race conditions.
        # Note (2): Instead of interfering with the main file directly, the new content is written to a temp file before
        #           swapping with the real file to minimize the I/O block.

        configuration = ConfigurationWrapper.migrate(configuration)

        # Perform sanity checks
        for context_name, context in configuration.contexts.items():
            duplicate_endpoint_id_count_map = dict()
            for endpoint in context.endpoints:
                if endpoint.id not in duplicate_endpoint_id_count_map:
                    duplicate_endpoint_id_count_map[endpoint.id] = 0
                duplicate_endpoint_id_count_map[endpoint.id] += 1
            duplicate_endpoint_ids = sorted([id for id, count in duplicate_endpoint_id_count_map.items() if count > 1])
            assert len(duplicate_endpoint_ids) == 0, \
                f'Detected at least two endpoints with the same ID ({", ".join(duplicate_endpoint_ids)}) '\
                f'in the "{context_name}" context'

        # Save the changes.
        new_content = yaml.dump(configuration.dict(exclude_none=True), Dumper=yaml.SafeDumper)
        if not os.path.exists(os.path.dirname(self.__swap_file_path)):
            os.makedirs(os.path.dirname(self.__swap_file_path), exist_ok=True)
        with open(self.__swap_file_path, 'w') as f:
            f.write(new_content)
        shutil.copyfile(self.__swap_file_path, self.__file_path)
        os.unlink(self.__swap_file_path)
