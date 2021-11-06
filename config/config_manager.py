import json
import os

from utils.exceptions import InvalidConfigArgument


class ConfigManager:

    CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'configuration.json')

    def __init__(self):
        self.config_data = None
        self.config_data_loader()

    def config_data_loader(self):
        with open(self.CONFIG_FILE, 'r') as file:
            self.config_data = json.load(file)


class ConfigUpdater(ConfigManager):

    def __init__(self):
        super().__init__()

    def view(self) -> None:
        self._recursive_view(self.config_data)

    # TODO: You tried getting fancy. Fix This.
    def _recursive_view(self, d):
        print('\n')
        for k, v in d.items():
            if isinstance(v, dict):
                print(f'====={k}====')
                self._recursive_view(v)
            else:
                print(f'{k}...{v}')

    def update(self, param: str, val: str) -> None:
        if param.upper() == 'TEST_ON':
            if self._validate_test(val):
                self.config_data[param] = val.upper()
            else:
                raise InvalidConfigArgument('Value must be TRUE or FALSE')
        elif param.upper() == "CONCURRENT_SESSIONS":
            self.config_data[param] = int(val)

        self._config_save()

    @staticmethod
    def _validate_test(val) -> bool:
        if val.upper() == 'TRUE' or 'FALSE':
            return True
        else:
            return False

    def _config_save(self) -> None:
        data = [self.config_data]
        with open(self.CONFIG_FILE, 'w') as file:
            json.dump(data, file, indent=2)


class ConfigFetch(ConfigManager):

    def __init__(self):
        super().__init__()

    def fetch_test_status(self) -> bool:
        if self.config_data['TEST_ON'] == 'TRUE':
            return True
        else:
            return False

    def fetch_current_env(self) -> dict:
        if self.fetch_test_status():
            return self._package_paths(self.config_data['ENV']['TEST_RESOURCES'])
        else:
            return self._package_paths(self.config_data['ENV']['PROD_RESOURCES'])

    def _package_paths(self, env: dict) -> dict:
        packaged_env = dict()
        for k, v in env.items():
            if k == 'TIMER_DB_PATH':
                packaged_env['DB_PATH'] = self._compile_path(v)
            else:
                packaged_env['SESSION_PATH'] = self._compile_path(v)

        return packaged_env

    def _compile_path(self, file: str) -> os:
        return os.path.join(self.config_data["PROJECT_PATH"], file)
