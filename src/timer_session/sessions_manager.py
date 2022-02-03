import json
from datetime import datetime
from typing import Union

from .session import Session
from src.config.config_manager import ConfigFetch
from .session_datetime_converter import DateTimeConverter
from src.utils.command_enums import InputType


SESSION_JSON_PATH = ConfigFetch().fetch_session_path()


class SessionManager:

    def __init__(self):
        self.sessions = list()

    def add_session(self, session: Session):
        self.sessions.append(session)
        self.sessions.sort(key=lambda x: x.project_id)

    def get_current_session(self):
        if len(self.sessions) == 0:
            return None
        else:
            self.sessions.sort(key=lambda x: x.current_session)
            current_session = self.sessions[-1]
            self.sessions.sort(key=lambda x: x.project_id)
            return current_session

    def export_sessions_to_json(self):
        export = ExportSessionsToJSON(self.sessions)
        export.dump_sessions_to_json()

    def remove_session(self, pid: int):
        session_to_remove= self._session_bin_search(pid)
        if session_to_remove != -1:
            print('Hello')
            self.sessions.pop(session_to_remove)
            print(self.sessions)
        else:
            raise KeyError('Session to remove not found')

    def display_sessions(self):
        print('\n-- Current Sessions --')
        for session in self.sessions:
            print(f'{session.project_name} --- {session.project_id}')

    def switch_current_session(self, pid: int):
        current = self.get_current_session()
        if current is not None:
            find_session = self._session_bin_search(pid)
            if find_session != -1:
                new_current_session = self.sessions[find_session]
                if current == new_current_session:
                    print(f'{current.project_name} is already current')
                else:
                    new_current_session.current_session = True
                    current.current_session = False
            else:
                raise KeyError(f'Project ID #{pid} is not in sessions.')
        else:
            raise KeyError('No Current Session found')

    def _session_bin_search(self, project_id: int) -> int:
        """Binary search function for session. Will return index if session exists; return -1 if not exists"""
        left, right = 0, len(self.sessions) - 1
        self.sessions = sorted(self.sessions, key=lambda x: x.project_id)
        while left <= right:
            mid = (left + right) // 2
            if self.sessions[mid].project_id == project_id:
                return mid
            elif self.sessions[mid].project_id > project_id:
                right = mid - 1
            else:
                left = mid + 1
        return -1

    def stop_select_new_current_session(self) -> Union[int, None]:
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

        elif len(self.sessions) == 0:
            return None

    def check_for_session(self, pid: int):
        search = self._session_bin_search(pid)
        if search != -1:
            return True
        else:
            return False

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
        elif k == '_current_session':
            if v == 1:
                data[k] = True
            elif v == 0:
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
        if self._session_data:
            for s in self._session_data:
                attr = self.convert_session_obj_to_dict_for_json(s)
                sessions.append(attr)
                with open(SESSION_JSON_PATH, 'w') as file:
                    json.dump(sessions, file, indent=2)
        else:
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
    def convert_session_data_to_valid_json(val: Union[InputType, bool, datetime, None]) -> Union[str, int]:
        if val is None:
            return 'None'
        elif isinstance(val, datetime):
            return DateTimeConverter(val).get_datetime_str()
        elif isinstance(val, InputType):
            return val.name
        elif isinstance(val, bool):
            if val:
                return 1
            else:
                return 0


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
        self._current_session = 0

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
