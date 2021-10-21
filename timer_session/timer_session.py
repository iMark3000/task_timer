import json
from datetime import datetime
from typing import Dict, Union

from utils.settings import SESSION_JSON_PATH
from utils.command_enums import InputType


class Session:
    """
    This class loads saved sessions data stored in json file and updates
    the data as needed.
    """

    JSON_PATH = SESSION_JSON_PATH

    def __init__(self):
        self._session_data = self._load_json_file()
        self._project_name = self._session_data['_project_name']
        self._last_command = self._session_data['_last_command']
        self._session_id = self._session_data["_session_id"]
        self._session_start_time = self._session_data["_session_start_time"]
        self._last_command_time = self._session_data["_last_command_time"]

    def _load_json_file(self) -> Dict:
        """Loads data from json file"""
        with open(self.__class__.JSON_PATH) as file:
            data = json.load(file)
        return data['session']

    def get_project_name(self):
        if self._project_name == 'None':
            return None
        else:
            return self._project_name

    def update_project_name(self, name):
        if self._project_name == 'None' or name == 'None':
            self._project_name = name
        else:
            pass  # Todo: Create Exception to raise?

    def get_session_id(self):
        if self._session_id == 'None':
            return None
        else:
            return self._session_id

    def update_session_id(self, sid):
        if self._session_id == 'None':
            self._session_id = sid
        else:
            pass  # Todo: Create Exception to raise?

    def get_session_start_time(self):
        if self._session_start_time == 'None':
            return None
        else:
            return DateTimeConverter(self._session_start_time).get_datetime_obj()

    def update_session_start_time(self, start_time):
        if self._session_start_time == 'None':
            self._session_start_time = DateTimeConverter(start_time).get_datetime_str()
        else:
            pass  # Todo: Create Exception to raise?

    def get_last_command_str(self):
        if self._last_command == 'NO_SESSION':
            return None
        else:
            return self._last_command.upper()

    def get_last_command_enum(self):
        if self._last_command == 'NO_SESSION':
            return None
        else:
            return InputType[self._last_command.upper()]

    def update_last_command(self, last_command):
        self._last_command = last_command

    def get_last_command_time(self):
        if self._last_command_time == 'None':
            return None
        else:
            return DateTimeConverter(self._last_command_time).get_datetime_obj()

    def update_last_command_time(self, last_command_time: datetime):
        self._last_command_time = DateTimeConverter(last_command_time).get_datetime_str()

    def get_session_data(self) -> dict:
        attrs = vars(self)
        return {k: v for k, v in attrs.items() if k != '_session_data'}


class DateTimeConverter:

    """
    JSON does not store Python datetime objects. Time is stored in JSON as %x_%X

    %x is the date
    %X is the time
    _ is the delimiter

    This class will convert a datetime object to this string format using strpftime() method
    and will convert strings in this format back to a datetime object.
    """

    def __init__(self, dt: Union[str, datetime]):
        if isinstance(dt, str):
            self.date_string = dt
            self.date_obj = self._convert_str_to_datetime_obj(dt)
        elif isinstance(dt, datetime):
            self.date_obj = dt
            self.date_string = self._convert_datetime_to_str(dt)

    def _convert_str_to_datetime_obj(self, dt) -> datetime:
        d, t = dt.split("_")
        day = self._parse_date_string(d)
        tm = self._parse_time_string(t)
        return datetime(day[2], day[0], day[1], hour=tm[0], minute=tm[1], second=tm[2])

    @staticmethod
    def _parse_date_string(d: str) -> list:
        d = d.split("/")
        return [int(x) for x in d]

    @staticmethod
    def _parse_time_string(t: str) -> list:
        t = t.split(":")
        return [int(x) for x in t]

    @staticmethod
    def _convert_datetime_to_str(dt: datetime) -> str:
        return dt.strftime("%x_%X")

    def get_datetime_obj(self) -> datetime:
        return self.date_obj

    def get_datetime_str(self) -> str:
        return self.date_string


# TODO: Determine is the below func is still needed
def reset_json_data() -> None:
    """Helper method to reset JSON file when a session is stopped"""
    session_data = dict()
    session_data["last_command"] = "NO_SESSION"
    session_data["project_name"] = "None"
    session_data["session_id"] = "None"
    session_data["session_start_time"] = "None"
    session_data["last_command_time"] = "None"
    data = {"session": session_data}
    with open(SESSION_JSON_PATH) as file:
        json.dump(data, file, indent=2)


def write_session_json_data(session: Session) -> None:
    """Helper func that writes session data to JSON file"""
    session_data = session.get_session_data()
    data = {"session": session_data}
    with open(SESSION_JSON_PATH, 'w') as file:
        json.dump(data, file, indent=2)
