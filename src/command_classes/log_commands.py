from abc import abstractmethod
from datetime import datetime

from src.command_classes.commands_base_class import CommandBaseClass
from src.utils.command_enums import InputType
from src.utils.exceptions import TimeSequenceError, CommandSequenceError


class LogCommand(CommandBaseClass):
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

    def validate_time(self, previous_command_time: InputType):
        if previous_command_time:
            if self._time < previous_command_time:
                raise TimeSequenceError('Error: New time is before old time')
            elif self._time > datetime.now():
                raise TimeSequenceError('Error: Cannot enter a time in the future')


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