import json
import os

from .configurations import TEST_CONFIGURATION
from .configurations import PRODUCTION_CONFIGURATION
from .configurations import PROJECT_PATH


class ConfigManager:

    STORED_CONFIG_VARS = os.path.join(os.path.dirname(__file__), 'configuration.json')

    def __init__(self):
        self.config_data = None
        self._test_on = None
        self.config_set()

    def config_set(self):
        config_vars = self.config_var_loader()

        self._test_on = config_vars["test_on"]

        if self._test:
            self.config_data = PRODUCTION_CONFIGURATION
            self.config_data.update(config_vars["test_vars"])
        else:
            self.config_data = TEST_CONFIGURATION
            self.config_data.update(config_vars["production_vars"])
        self.config_data["test_on"] = config_vars["test_on"]

    def config_var_loader(self):
        with open(self.STORED_CONFIG_VARS, 'r') as file:
            data = json.load(file)
            return data[0]

    def _test(self):
        if self._test_on == 0:
            return False
        else:
            return True


class ConfigUpdater(ConfigManager):

    def __init__(self):
        super().__init__()

    def view(self) -> None:
        if self._test():
            print("TEST MODE ON")
        else:
            print("PRODUCTION MODE ON")
        for k, v in self.config_data.items():
            if "auto" in k:
                if v == 0:
                    self._print_config(k, "False")
                else:
                    self._print_config(k, "True")
            elif "PATH" in k:
                self._print_config(k, os.path.join(PROJECT_PATH, v))
            else:
                pass

    @staticmethod
    def _print_config(k, value):
        print(f'{k}: {value}')

    def toggle_param(self, param):
        TOGGLE_PARAMS = {"test": "test_on", "fetch": "auto_fetch", "switch": "auto_switch"}

        test_flag = False

        if param == "test":
            test_flag = True

        if param.lower() in TOGGLE_PARAMS.keys():
            if self.config_data[TOGGLE_PARAMS[param]] == 0:
                self.config_data[TOGGLE_PARAMS[param]] = 1
                print(f'{TOGGLE_PARAMS[param].upper()} toggled on.')
            else:
                self.config_data[TOGGLE_PARAMS[param]] = 0
                print(f'{TOGGLE_PARAMS[param].upper()} toggled off.')

        self._config_save(test_flag)

    def _config_save(self, test_flag) -> None:
        data = self.config_var_loader()

        if test_flag:
            data["test_on"] = self.config_data["test_on"]
        else:
            if self._test():
                key = "test_vars"
            else:
                key = "production_vars"
            for k in data[key].keys():
                data[key][k] = self.config_data[k]

        with open(self.STORED_CONFIG_VARS, 'w') as file:
            data = [data]
            json.dump(data, file, indent=2)


class ConfigFetch(ConfigManager):

    def __init__(self):
        super().__init__()

    def fetch_test_status(self) -> bool:
        return self._test()

    def fetch_session_path(self):
        return os.path.join(PROJECT_PATH, self.config_data["SESSION_JSON_PATH"])

    def fetch_db_path(self):
        return os.path.join(PROJECT_PATH, self.config_data["TIMER_DB_PATH"])
