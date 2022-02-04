
from .command_factory_base_class import CommandAbstractFactory

from ...command_classes.log_commands import StartCommand, PauseCommand, ResumeCommand, StopCommand

from src.utils.command_enums import InputType


class LogCommandFactory(CommandAbstractFactory):

    def __init__(self, command: InputType, command_args: dict):
        self.command = command
        self.command_args = command_args

    def create_command(self):
        if self.command == InputType.START:
            return StartCommand(self.command, **self.command_args)
        elif self.command == InputType.RESUME:
            return ResumeCommand(self.command, **self.command_args)
        elif self.command == InputType.PAUSE:
            return PauseCommand(self.command, **self.command_args)
        elif self.command == InputType.STOP:
            return StopCommand(self.command, **self.command_args)
