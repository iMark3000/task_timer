from abc import ABC, abstractmethod

from .commands import *
from utils.const import LOG_COMMANDS
from utils.const import UTILITY_COMMANDS
from utils.const import QUERY_COMMANDS
from utils.exceptions import NoProjectNameProvided


class CommandAbstractFactory(ABC):

    @abstractmethod
    def create_command(self):
        pass


class LogCommandFactory(CommandAbstractFactory):

    def __init__(self, command_dict: dict):
        self.command = command_dict['command']
        self.command_time = command_dict['command_args'].time
        self.project_name = command_dict['command_args'].name

    def create_command(self):
        if self.command == InputType.START:
            return self._create_start_command()
        else:
            return self._create_log_command()

    def _create_start_command(self):
        return StartCommand(self.command, self.project_name, self.command_time)

    def _create_log_command(self):
        if self.command == InputType.RESUME:
            return ResumeCommand(self.command, self.command_time)
        elif self.command == InputType.PAUSE:
            return PauseCommand(self.command, self.command_time)
        elif self.command == InputType.STOP:
            return StopCommand(self.command, self.command_time)


class QueryCommandFactory(CommandAbstractFactory):

    def __init__(self, command_dict: dict):
        self.command = command_dict['command']

    def create_command(self):
        pass


class UtilityCommandFactory(CommandAbstractFactory):

    def __init__(self, command_dict: dict):
        self.command = command_dict['command']
        self.project_id = command_dict['command_args'].project_id
        self.project_name = command_dict['command_args'].project_name

    def create_command(self) -> UtilityCommand:
        if self.command == InputType.FETCH:
            return FetchProject(self.command, project_id=self.project_id)
        if self.command == InputType.NEW:
            return NewCommand(self.command, project_name=self.project_name)
        elif self.command == InputType.STATUS:
            return StatusCheck(self.command)


def command_factory_router(command_dict: dict):
    command = command_dict['command']
    if command in LOG_COMMANDS:
        command_obj = LogCommandFactory(command_dict).create_command()
        return command_obj
    elif command in QUERY_COMMANDS:
        command_obj = QueryCommandFactory(command_dict).create_command()
        return command_obj
    elif command in UTILITY_COMMANDS:
        command_obj = UtilityCommandFactory(command_dict).create_command()
        return command_obj
