import json
from datetime import datetime
from typing import Union

from utils.settings import SESSION_JSON_PATH
from utils.command_enums import InputType
from utils.const import LOG_COMMANDS


class Session:
    """
    This class holds data loaded from the current_session json file and updates
    the data as needed.

    Session objects are instantiated by the create_session() method.
    """

    def __init__(self, data) -> None:
        self._project_name = data['_project_name']
        self._project_id = data['_project_id']
        self._last_command = data['_last_command']
        self._session_id = data["_session_id"]
        self._session_start_time = data["_session_start_time"]
        self._last_command_time = data["_last_command_time"]
        self._last_command_log_note = data["_last_command_log_note"]

    @property
    def project_name(self) -> Union[str, None]:
        if self._project_name == 'None':
            return None
        else:
            return self._project_name

    @project_name.setter
    def project_name(self, name: str) -> None:
        self._project_name = name

    @property
    def project_id(self) -> Union[str, None]:
        if self._project_id == 'None':
            return None
        else:
            return self._project_id

    @project_id.setter
    def project_id(self, pid: int) -> None:
        self._project_id = pid

    @property
    def session_id(self) -> Union[str, int, None]:
        if self._session_id == 'None':
            return None
        else:
            return self._session_id

    @session_id.setter
    def session_id(self, sid: Union[int, str]) -> None:
        self._session_id = sid

    @property
    def session_start_time(self) -> Union[datetime, None]:
        if self._session_start_time == 'None':
            return None
        else:
            return DateTimeConverter(self._session_start_time).get_datetime_obj()

    @session_start_time.setter
    def session_start_time(self, start_time: Union[str, datetime]) -> None:
        self._session_start_time = DateTimeConverter(start_time).get_datetime_str()

    @property
    def last_command(self) -> InputType:
        return InputType[self._last_command.upper()]

    @last_command.setter
    def last_command(self, last_command: InputType) -> None:
        if last_command in LOG_COMMANDS:
            self._last_command = last_command.name

    @property
    def last_command_time(self) -> Union[datetime, None]:
        if self._last_command_time == 'None':
            return None
        else:
            return DateTimeConverter(self._last_command_time).get_datetime_obj()

    @last_command_time.setter
    def last_command_time(self, last_command_time: datetime) -> None:
        self._last_command_time = DateTimeConverter(last_command_time).get_datetime_str()
        
    @property
    def log_note(self):
        if self._last_command_log_note == 'None':
            return None
        else:
            return self._last_command_log_note
    
    @log_note.setter
    def log_note(self, note):
        self._last_command_log_note = note

    def export_session_data(self) -> dict:
        attrs = vars(self)
        return {k: v for k, v in attrs.items()}


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
        return dt.strftime("%m/%d/%Y_%X")

    def get_datetime_obj(self) -> datetime:
        return self.date_obj

    def get_datetime_str(self) -> str:
        return self.date_string


def create_session() -> Session:
    """Helper func that loads session data from JSON file and creates Session obj"""
    with open(SESSION_JSON_PATH, 'r') as file:
        data = json.load(file)
    return Session(data['session'])


def write_session_data_to_json(session: Session) -> None:
    """Helper func that writes session data to JSON file"""
    session_data = session.export_session_data()
    data = {"session": session_data}
    with open(SESSION_JSON_PATH, 'w') as file:
        json.dump(data, file, indent=2)


def fetch_helper_func(session: Session, project_name: str, pid: int) -> None:
    if session.last_command == InputType.NO_SESSION:
        session.project_id = pid
        session.project_name = project_name
    else:
        print(session.last_command)
        print('Session in progress, cannot fetch another project at this time.')  # Todo: Create Exception to raise?


def reset_json_data() -> None:
    """Helper method to reset JSON file when a session is stopped"""
    session_data = dict()
    session_data["_last_command"] = "NO_SESSION"
    session_data["_project_name"] = "None"
    session_data["_project_id"] = "None"
    session_data["_session_id"] = "None"
    session_data["_session_start_time"] = "None"
    session_data["_last_command_time"] = "None"
    session_data["_last_command_log_note"] = "None"
    data = {"session": session_data}
    with open(SESSION_JSON_PATH, 'w') as file:
        json.dump(data, file, indent=2)
