from abc import ABC, abstractmethod
from datetime import datetime
from typing import Union

from utils.exceptions import CommandSequenceError
from utils.command_enums import InputType


class Command(ABC):
    """Abstract Base Class for all command classes"""
    def __init__(self, command: InputType, **kwargs):
        self._command = command
        for k, v in kwargs.items():
            if f'_{k}' in self.__dict__.keys():
                self.__dict__[f'_{k}'] = v

    @property
    def command(self):
        return self._command

    def get_command_name(self):
        return self._command.name

    def __str__(self):
        return f'{self.command}: {self.__dict__}'


# ~~~~~~~~~~~LOG COMMAND FAMILY~~~~~~~~~~~~~~~~~~~~
# Log Commands log time entries to the database

class LogCommand(Command):
    """Base Class for Log Commands"""
    def __init__(self, command: InputType, **kwargs):
        self._time = None
        self._log_note = None
        super().__init__(command, **kwargs)

    @property
    def time(self):
        return self._time

    @property
    def log_note(self):
        return self._log_note

    @abstractmethod
    def validate_sequence(self, previous_command: InputType):
        pass


class StartCommand(LogCommand):

    def __init__(self, command: InputType, **kwargs):
        self._project_name = None
        self._session_note = None
        super().__init__(command, **kwargs)

    # Todo: Is a setter method needed for project_name?
    @property
    def project_name(self):
        return self._project_name

    @property
    def session_note(self):
        return self._session_note

    def validate_sequence(self, previous_command):
        if previous_command != InputType.NO_SESSION:
            # TODO: How many different modules raise this error? Is it raised in the handler?
            raise CommandSequenceError(f"Stop current session first before starting new Session")


class PauseCommand(LogCommand):

    def __init__(self, command: InputType, **kwargs):
        super().__init__(command, **kwargs)

    def validate_sequence(self, previous_command):
        if previous_command != InputType.START and previous_command != InputType.RESUME:
            raise CommandSequenceError(f"Session already paused or no session in progress")


class ResumeCommand(LogCommand):

    def __init__(self, command: InputType, **kwargs):
        super().__init__(command, **kwargs)

    def validate_sequence(self, previous_command):
        if previous_command != InputType.PAUSE:
            if previous_command == InputType.NO_SESSION:
                raise CommandSequenceError(f"No session in progress")
            elif previous_command == InputType.RESUME or previous_command == InputType.START:
                raise CommandSequenceError(f"Session already in progress")


class StopCommand(LogCommand):

    def __init__(self, command: InputType, **kwargs):
        super().__init__(command, **kwargs)

    def validate_sequence(self, previous_command):
        if previous_command == InputType.NO_SESSION:
            raise CommandSequenceError(f"No session in progress")


# ~~~~~~~~~~~QUERY COMMAND FAMILY~~~~~~~~~~~~~~~~~~~~
# Query commands query the database via the query module

class QueryCommand(Command):

    def __init__(self, command: InputType):
        super().__init__(command)
        self.dataset = None

    @property
    def dataset(self):
        return self.dataset

    @dataset.setter
    def dataset(self, dataset):
        self.dataset = dataset


# ~~~~~~~~~~~UPDATE COMMAND FAMILY~~~~~~~~~~~~~~~~~~~~
# Update commands update records in the database

class UpdateCommand(Command):
    pass


class DeactivateCommand(UpdateCommand):
    pass


class ReactivateCommand(UpdateCommand):
    pass


class EditCommand(UpdateCommand):
    pass


class MergeCommand(UpdateCommand):
    pass


class RenameCommand(UpdateCommand):
    pass


# ~~~~~~~~~~~UTILITY COMMAND FAMILY~~~~~~~~~~~~~~~~~~~~
# Utility commands are helper commands that add
# functionality or make small db queries but do not
# update the database

class UtilityCommand(Command):

    def __init__(self, command: InputType, **kwargs):
        super().__init__(command, **kwargs)


class StatusCheck(UtilityCommand):

    def __init__(self, command: InputType, **kwargs):
        self._all = False
        super().__init__(command, **kwargs)

    def is_all(self):
        return self._all


class UtilityProjectsCommands(UtilityCommand):

    def __init__(self, command: InputType, **kwargs):
        self._project_name = None
        super().__init__(command, **kwargs)

    @property
    def project_name(self):
        return self._project_name


class ProjectsCommand(UtilityProjectsCommands):

    def __init__(self, command: InputType, **kwargs):
        self._all = False
        self._filter_by = None
        super().__init__(command, **kwargs)

    def is_all(self):
        return self._all

    @property
    def filter_by(self):
        return self._filter_by


class NewCommand(UtilityProjectsCommands):

    def __init__(self, command: InputType, **kwargs):
        super().__init__(command, **kwargs)


class SessionUtilityCommands(UtilityCommand):

    def __init__(self, command: InputType, **kwargs):
        self._project_id = None
        super().__init__(command, **kwargs)

    @property
    def project_id(self):
        return self._project_id


class FetchProject(SessionUtilityCommands):

    def __init__(self, command: InputType, **kwargs):
        super().__init__(command, **kwargs)


class SwitchCommand(SessionUtilityCommands):

    def __init__(self, command: InputType, **kwargs):
        super().__init__(command, **kwargs)


# ~~~~~~~~~~~CONFIG COMMAND FAMILY~~~~~~~~~~~~~~~~~~~~
# This command did not feel like it fell under any of the
# other groups

class ConfigCommand(Command):

    def __init__(self, command: InputType, **kwargs):
        self.view = None
        self.config_key = None
        self.config_value = None
        super().__init__(command, **kwargs)

    def is_view(self):
        return self.view

    def get_key(self) -> Union[str, None]:
        return self.config_key

    def get_value(self) -> Union[str, int, None]:
        return self.config_value
