import datetime
from abc import ABC, abstractmethod

from utils.time_string_converter import TimeStringToDateTimeObj
from utils.exceptions import CommandSequenceError, TimeError
from utils.command_enums import InputType


class Command(ABC):

    @abstractmethod
    def get_command_type(self):
        pass


class LogCommand(Command):

    def __init__(self, command: InputType, time=None):
        self.command = command
        self.time = time
        self._set_command_time()

    def get_command_type(self):
        return self.command

    def _set_command_time(self):
        if self.time:
            try:
                self.time = TimeStringToDateTimeObj(self.time).get_datetime_obj()
            except TimeError as error:
                print(error)
        else:
            self.time = datetime.datetime.now()

    def get_command_time(self):
        return self.time

    @abstractmethod
    def validate_sequence(self, previous_command: InputType):
        pass


class StartCommand(LogCommand):

    def __init__(self, command: InputType, name, time=None):
        self.name = name
        super().__init__(command, time=time)

    def get_project_name(self):
        return self.name

    def validate_sequence(self, previous_command):
        if previous_command != InputType.NO_SESSION:
            raise CommandSequenceError(f"Stop current session first before starting new Session")


class PauseCommand(LogCommand):

    def __init__(self, command: InputType, time=None):
        super().__init__(command, time=time)

    def validate_sequence(self, previous_command):
        if previous_command != InputType.START or previous_command != InputType.RESUME:
            raise CommandSequenceError(f"Session already paused or no session in progress")


class ResumeCommand(LogCommand):

    def __init__(self, command: InputType, time=None):
        super().__init__(command, time=time)

    def validate_sequence(self, previous_command):
        if previous_command != InputType.PAUSE:
            if previous_command == InputType.NO_SESSION:
                raise CommandSequenceError(f"No session in progress")
            elif previous_command == InputType.RESUME:
                raise CommandSequenceError(f"Session already in progress")


class StopCommand(LogCommand):

    def __init__(self, command: InputType, time=None):
        super().__init__(command, time=time)

    def validate_sequence(self, previous_command):
        if previous_command == InputType.NO_SESSION:
            raise CommandSequenceError(f"No session in progress")


class QueryCommand(Command):
    pass


class GetStatus(Command):
    pass
