from abc import ABC, abstractmethod
import datetime

from utils.exceptions import CommandSequenceError, TimeSequenceError
from utils.command_enums import InputType


class Command(ABC):

    def __init__(self, command: InputType):
        self.command = command

    def get_command_type(self):
        return self.command

    def get_command_name(self):
        return self.command.name


class LogCommand(Command):

    def __init__(self, command: InputType, time):
        self.time = time
        super().__init__(command)

    def get_command_time(self):
        return self.time

    @abstractmethod
    def validate_sequence(self, previous_command: InputType):
        pass


class StartCommand(LogCommand):

    def __init__(self, command: InputType, name, time):
        self.name = name
        super().__init__(command, time)

    def get_project_name(self):
        return self.name

    def validate_sequence(self, previous_command):
        if previous_command != InputType.NO_SESSION:
            raise CommandSequenceError(f"Stop current session first before starting new Session")


class PauseCommand(LogCommand):

    def __init__(self, command: InputType, time):
        super().__init__(command, time)

    def validate_sequence(self, previous_command):
        if previous_command != InputType.START or previous_command != InputType.RESUME:
            raise CommandSequenceError(f"Session already paused or no session in progress")


class ResumeCommand(LogCommand):

    def __init__(self, command: InputType, time):
        super().__init__(command, time)

    def validate_sequence(self, previous_command):
        if previous_command != InputType.PAUSE:
            if previous_command == InputType.NO_SESSION:
                raise CommandSequenceError(f"No session in progress")
            elif previous_command == InputType.RESUME:
                raise CommandSequenceError(f"Session already in progress")


class StopCommand(LogCommand):

    def __init__(self, command: InputType, time):
        super().__init__(command, time)

    def validate_sequence(self, previous_command):
        if previous_command == InputType.NO_SESSION:
            raise CommandSequenceError(f"No session in progress")


class QueryCommand(Command):

    def __init__(self, command: InputType):
        super().__init__(command)


class FetchProject(QueryCommand):

    def __init__(self, command: InputType, project_id):
        self.project_id = project_id
        super().__init__(command)

    def get_project_id(self):
        return self.project_id

    @staticmethod
    def validate_sequence(previous_command):
        if previous_command != InputType.NO_SESSION:
            raise CommandSequenceError("Unable to fetch project with Session in progress")


class ProjectsCommand(QueryCommand):
    pass


class GetStatus(QueryCommand):
    pass
