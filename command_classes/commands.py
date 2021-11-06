from abc import ABC, abstractmethod
from datetime import datetime

from utils.exceptions import CommandSequenceError
from utils.command_enums import InputType


class Command(ABC):
    """Abstract Base Class for all command classes"""
    def __init__(self, command: InputType):
        self.command = command

    def get_command_type(self):
        return self.command

    def get_command_name(self):
        return self.command.name


# ~~~~~~~~~~~LOG COMMAND FAMILY~~~~~~~~~~~~~~~~~~~~
# Log Commands log time entries to the database

class LogCommand(Command):
    """Base Class for Log Commands"""
    def __init__(self, command: InputType, time: datetime, log_note):
        self.time = time
        self._log_note = log_note
        super().__init__(command)

    def get_command_time(self):
        return self.time

    def get_log_note(self):
        return self._log_note

    @abstractmethod
    def validate_sequence(self, previous_command: InputType):
        pass


class StartCommand(LogCommand):

    def __init__(self, command: InputType, name: str, time: datetime, log_note: str, session_note: str):
        self.name = name
        self._session_note = session_note
        super().__init__(command, time, log_note)

    def get_project_name(self):
        return self.name

    def get_session_note(self):
        return self._session_note

    def validate_sequence(self, previous_command):
        if previous_command != InputType.NO_SESSION:
            # TODO: How many different modules raise this error? Is it raised in the handler?
            raise CommandSequenceError(f"Stop current session first before starting new Session")


class PauseCommand(LogCommand):

    def __init__(self, command: InputType, time: datetime, log_note: str):
        super().__init__(command, time, log_note)

    def validate_sequence(self, previous_command):
        if previous_command != InputType.START and previous_command != InputType.RESUME:
            raise CommandSequenceError(f"Session already paused or no session in progress")


class ResumeCommand(LogCommand):

    def __init__(self, command: InputType, time, log_note: str):
        super().__init__(command, time, log_note)

    def log_note(self):
        return self.log_note()

    def validate_sequence(self, previous_command):
        if previous_command != InputType.PAUSE:
            if previous_command == InputType.NO_SESSION:
                raise CommandSequenceError(f"No session in progress")
            elif previous_command == InputType.RESUME or previous_command == InputType.START:
                raise CommandSequenceError(f"Session already in progress")


class StopCommand(LogCommand):

    def __init__(self, command: InputType, time, log_note: str):
        super().__init__(command, time, log_note)

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

    def __init__(self, command: InputType):
        super().__init__(command)


class ConfigCommand(UtilityCommand):
    pass


class ProjectsCommand(UtilityCommand):
    pass


class StatusCheck(UtilityCommand):

    def __init__(self, command: InputType):
        super().__init__(command)


class FetchProject(UtilityCommand):

    def __init__(self, command: InputType, project_id=None, project_name=None):
        self.project_id = project_id
        self.project_name = project_name
        super().__init__(command)

    def get_project_name(self):
        return self.project_name

    def get_project_id(self):
        return self.project_id

    @staticmethod
    def validate_sequence(previous_command):
        if previous_command != InputType.NO_SESSION:
            raise CommandSequenceError("Unable to fetch project with Session in progress")


class NewCommand(UtilityCommand):

    def __init__(self, command: InputType, project_id=None, project_name=None):
        self.project_id = project_id
        self.project_name = project_name
        super().__init__(command)

    def get_project_name(self):
        return self.project_name

    def get_project_id(self):
        return self.project_id


class SwitchCommand(UtilityCommand):
    pass
