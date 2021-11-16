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
            data = json.load(file)
            self.config_data = data[0]


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
        if param:
            if param.upper() not in self.config_data.keys():
                raise KeyError(f'{param} is not a configuration')
            elif param.upper() == 'TEST_ON':
                if self._validate_test(val):
                    self.config_data[param.upper()] = val.upper()
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
            paths = self._package_paths(self.config_data['ENV']['TEST_RESOURCES']["PATHS"])
            concurrent_sessions = self.config_data['ENV']['TEST_RESOURCES']['CONCURRENT_SESSIONS']
        else:
            paths = self._package_paths(self.config_data['ENV']['PROD_RESOURCES']["PATHS"])
            concurrent_sessions = self.config_data['ENV']['PROD_RESOURCES']['CONCURRENT_SESSIONS']

        return {'CONCURRENT_SESSIONS': concurrent_sessions, 'PATHS': paths}

    def _package_paths(self, env: dict) -> dict:
        packaged_env_paths = dict()
        for k, v in env.items():
            if k == 'TIMER_DB_PATH':
                packaged_env_paths['DB_PATH'] = self._compile_path(v)
            else:
                packaged_env_paths['SESSION_PATH'] = self._compile_path(v)

        return packaged_env_paths

    def _compile_path(self, file: str) -> os:
        return os.path.join(self.config_data["PROJECT_PATH"], file)
