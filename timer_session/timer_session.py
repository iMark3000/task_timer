import json
import datetime
from typing import Union

from .time_log_stack import TimeLogStack
from utils.settings import SESSION_JSON_PATH


# noinspection SpellCheckingInspection
class Session:

    JSON_PATH = SESSION_JSON_PATH

    def __init__(self):
        self.session = self._load_file()
        self.timelog = self._setup_stack()

    def _load_file(self) -> dict:
        with open(self.__class__.JSON_PATH) as file:
            data = json.load(file)
        return data["session"]

    def _setup_stack(self) -> TimeLogStack:
        if self.session["timeLog"]:
            return TimeLogStack(tms=self.session["timeLog"])
        else:
            return TimeLogStack()

    def get_last_action(self) -> str:
        return self.session["lastAction"]

    def get_last_action_time(self) -> str:
        return self.timelog.get_last_action_time()

    def get_project(self) -> str:
        return self.session["project"]

    def get_time_log(self) -> list[datetime]:
        return self.timelog.get_stack_data()

    def _update_last_action(self, action: str) -> None:
        self.session["LastAction"] = action

    def _update_project(self, name: str) -> None:
        self.session["project"] = name

    def add_time_entry(self, tm: Union[str, datetime]) -> None:
        self.timelog.add_time(tm)


def reset_json_data(session: Session) -> None:
    session_data = dict()
    session_data["lastAction"] = "None"
    session_data["projectName"] = "None"
    session_data["timeLog"] = []
    data = {"session": session_data}
    with open(session.__class__.JSON_PATH) as file:
        json.dump(data, file, indent=2)


def write_session_json_data(session: Session) -> None:
    session_data = dict()
    session_data["lastAction"] = session.get_last_action()
    session_data["project"] = session.get_project()
    session_data["timeLog"] = session.get_time_log()
    data = {"session": session_data}
    with open(session.__class__.JSON_PATH) as file:
        json.dump(data, file, indent=2)


def convert_datetime_to_str(logs: list[datetime]) -> list[list[str, str]]:
    converted_times = list()
    for log in logs:
        start = log[0].strftime("%x_%X")
        end = log[1].strftime("%x_%X")
        converted_times.append([start, end])

    return converted_times


def package_for_database(session: Session):
    package = dict()
    package['Project'] = session.get_project()
    logs = session.get_time_log()
    package["logs"] = [tuple(x) for x in logs]
    return package
