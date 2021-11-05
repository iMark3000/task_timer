import json
import os

from utils.exceptions import ConfigurationNotFound
from utils.exceptions import InvalidConfigArgument


class ConfigManager:

    CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'configuration.json')

    def __init__(self):
        self.config_data = None
        self.config_data_loader()

    def config_data_loader(self):
        with open(self.CONFIG_FILE, 'r') as file:
            data = json.load(file)
        self.config_data = data[0]


class ConfigUpdater(ConfigManager):

    def __init__(self):
        super().__init__()

    def view(self):
        for k, v in self.config_data.items():
            print(f'{k}...{v}')

    def update(self, param, val):
        if param in self.config_data.keys():
            if param == 'TEST_ON':
                if self._validate_test(val):
                    self.config_data[param] = val.upper()
                else:
                    raise InvalidConfigArgument('Value must be TRUE or FALSE')
            else:
                self.config_data[param] = val
        else:
            raise ConfigurationNotFound(f'{param} does not exist.')
        self._config_save()

    @staticmethod
    def _validate_test(val):
        if val.upper() == 'TRUE' or 'FALSE':
            return True
        else:
            return False

    def _config_save(self):
        data = [self.config_data]
        with open(self.CONFIG_FILE, 'w') as file:
            json.dump(data, file, indent=2)


class ConfigFetch(ConfigManager):

    def __init__(self):
        super().__init__()

    def fetch(self, key):
        try:
            if key == 'TEST_ON':
                return self.config_data[key].upper()
            else:
                return self._compile_path(self.config_data[key])
        except KeyError:
            raise ConfigurationNotFound(f'{key} is not in the configuration.')

    def _compile_path(self, file):
        return os.path.join(self.config_data["PROJECT_PATH"], file)
