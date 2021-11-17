import json
import math
from datetime import datetime
from typing import Union

from .session import Session
from config.config_manager import ConfigFetch
from .session_datetime_converter import DateTimeConverter
from utils.command_enums import InputType


SESSION_JSON_PATH = ConfigFetch().fetch_current_env()['PATHS']['SESSION_PATH']
CONCURRENT_SESSIONS = ConfigFetch().fetch_current_env()['CONCURRENT_SESSIONS']


class SessionManager:

    def __init__(self):
        self.sessions = list()

    def add_session(self, session: Session):
        if CONCURRENT_SESSIONS == 0 or len(self.sessions) < CONCURRENT_SESSIONS:
            self.sessions.append(session)

    def get_current_session(self):
        if len(self.sessions) == 0:
            return None
        else:
            self.sessions.sort(key=lambda x: x.current_session)
            current_session = self.sessions[-1]
            # Todo: Do you really want to make this assertion?
            assert current_session.current_session is True, "Current session must be True"
            self.sessions.sort(key=lambda x: x.project_id)
            return current_session

    def export_sessions_to_json(self):
        ExportSessionsToJSON(self.sessions).dump_sessions_to_json()

    def remove_session(self, pid: int):
        self.display_sessions()
        new_session_list = [x for x in self.sessions if x.project_id != pid]
        self.sessions = new_session_list
        self.display_sessions()

    def display_sessions(self):
        for session in self.sessions:
            print(f'{session.project_name} --- {session.project_id}')

    def switch_current_session(self, pid: int):
        current = self.get_current_session()
        if current is not None:
            current.current_session = False
            new_current = self._recursive_search(self.sessions, pid)
            if new_current is not None:
                new_current.current_session = True
            else:
                raise KeyError(f'Project ID #{pid} is not in sessions.')
        else:
            raise KeyError('No Current Session found')

    def determine_new_current_pid(self) -> Union[int, None]:
        """
        This method is called by STOP command. It is called right before the
        current session that is being stopped is removed from self.sessions.
        The project ID that is returned is then passed to the switch_current_session()
        method.

        If len of self.sessions is 1, the method returns None because that is
        the current session, which is about to be removed.
        """
        if len(self.sessions) > 1:
            session_with_last_command_time = [x for x in self.sessions if x.current_session is False and
                                      x.last_command_time is not None]
            if session_with_last_command_time:
                session_with_last_command_time.sort(key=lambda x: x.last_command_time)
                pid = session_with_last_command_time[0].project_id
                return pid
            else:
                self.sessions.sort(key=lambda x: x.current_session)
                pid = self.sessions[0].project_id
                return pid

        elif len(self.sessions) == 1:
            return None

    def check_for_session(self, pid: int):
        if not self._recursive_search(self.sessions, pid):
            return False
        else:
            return True

    def _recursive_search(self, ls: list, pid: int):
        if len(ls) == 1:
            index = 0
        else:
            index = math.floor(len(ls) / 2)

        if pid == ls[index].project_id:
            return ls[index]
        elif index == 0:
            return False
        elif pid > ls[index].project_id:
            return self._recursive_search(ls[index:], pid)
        elif pid < ls[index].project_id:
            return self._recursive_search(ls[:index], pid)

    def count_of_concurrent_sessions(self):
        return len(self.sessions)


def start_manager():
    manager = SessionManager()
    data = load_session()
    for item in data:
        data = convert_data_for_session_object(item)
        session = create_session(data)
        manager.add_session(session)

    return manager


def create_session(data):
    return Session(**data)


def convert_data_for_session_object(data: dict) -> dict:
    for k, v in data.items():
        if k == '_last_command':
            data[k] = InputType[v]

        if 'time' in k and v != 'None':
            data[k] = DateTimeConverter(v).get_datetime_obj()
        elif v == 'None':
            data[k] = None
        elif v == 'True':
            data[k] = True
        elif v == 'False':
            data[k] = False

    return data


def load_session() -> list:
    with open(SESSION_JSON_PATH, 'r') as file:
        return json.load(file)


class ExportSessionsToJSON:

    def __init__(self, session_data: list):
        self._session_data = session_data

    def dump_sessions_to_json(self):
        sessions = list()
        for s in self._session_data:
            attr = self.convert_session_obj_to_dict_for_json(s)
            sessions.append(attr)
            with open(SESSION_JSON_PATH, 'w') as file:
                json.dump(sessions, file, indent=2)

    def convert_session_obj_to_dict_for_json(self, session: Session):
        obj_attr = dict()
        for attr in session.__slots__:
            value = getattr(session, attr)
            if isinstance(value, (datetime, InputType, bool)) or value is None:
                value = self.convert_session_data_to_valid_json(value)
            obj_attr[attr] = value
        return obj_attr

    @staticmethod
    def convert_session_data_to_valid_json(val: Union[InputType, bool, datetime, None]) -> str:
        if val is None:
            return 'None'
        elif isinstance(val, datetime):
            return DateTimeConverter(val).get_datetime_str()
        elif isinstance(val, InputType):
            return val.name
        elif isinstance(val, bool):
            if val:
                return 'True'
            else:
                return 'False'


class FetchSessionHelper:

    def __init__(self, project_name, project_id, session_manager: SessionManager):
        self._session_manager = session_manager
        self._project_name = project_name
        self._project_id = project_id
        self._last_command = "NO_SESSION"
        self._session_id = "None"
        self._session_start_time = "None"
        self._last_command_time = "None"
        self._last_command_log_note = "None"
        self._current_session = "False"

    def fetch(self):
        if self._should_be_active():
            self._current_session = "True"
        data = self._package_data()
        session = create_session(data)
        if not self._session_manager.check_for_session(session.project_id):
            self._session_manager.add_session(session)
            return True
        else:
            return False

    def _package_data(self):
        data = dict()
        for k, v in self.__dict__.items():
            if k != '_session_manager':
                data[k] = v

        return data

    def _should_be_active(self):
        if self._session_manager.count_of_concurrent_sessions() == 0:
            return True
