from datetime import datetime
from typing import Union

from src.utils.command_enums import InputType
from src.utils.const import LOG_COMMANDS


class Session:
    __slots__ = (
        '_project_name',
        '_project_id',
        '_last_command',
        '_session_id',
        '_session_start_time',
        '_last_command_time',
        '_last_command_log_note',
        '_current_session'
    )

    def __init__(self, **kwargs):
        self._project_name = kwargs['_project_name']
        self._project_id = kwargs['_project_id']
        self._last_command = kwargs['_last_command']
        self._session_id = kwargs['_session_id']
        self._session_start_time = kwargs['_session_start_time']
        self._last_command_time = kwargs['_last_command_time']
        self._last_command_log_note = kwargs['_last_command_log_note']
        self._current_session = kwargs['_current_session']

    @property
    def project_name(self) -> Union[str, None]:
        return self._project_name

    @project_name.setter
    def project_name(self, name: str) -> None:
        self._project_name = name

    @property
    def project_id(self) -> Union[int, None]:
        return self._project_id

    @project_id.setter
    def project_id(self, pid: int) -> None:
        self._project_id = pid

    @property
    def session_id(self) -> Union[int, None]:
        return self._session_id

    @session_id.setter
    def session_id(self, sid: int) -> None:
        self._session_id = sid

    @property
    def session_start_time(self) -> Union[datetime, None]:
        return self._session_start_time

    @session_start_time.setter
    def session_start_time(self, start_time: datetime) -> None:
        self._session_start_time = start_time

    @property
    def last_command(self) -> InputType:
        return self._last_command

    @last_command.setter
    def last_command(self, last_command: InputType) -> None:
        if last_command in LOG_COMMANDS:
            self._last_command = last_command

    @property
    def last_command_time(self) -> Union[datetime, None]:
        return self._last_command_time

    @last_command_time.setter
    def last_command_time(self, last_command_time: datetime) -> None:
        self._last_command_time = last_command_time
        
    @property
    def last_command_log_note(self) -> Union[str, None]:
        return self._last_command_log_note
    
    @last_command_log_note.setter
    def last_command_log_note(self, note: str) -> None:
        self._last_command_log_note = note

    @property
    def current_session(self):
        return self._current_session

    @current_session.setter
    def current_session(self, _bool: bool):
        self._current_session = _bool

    def __str__(self) -> str:
        return f'Session: {self._project_name} [{self._project_id}] -- Current? {self._current_session}'
