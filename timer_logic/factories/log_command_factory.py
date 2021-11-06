
from .command_factory_base_class import CommandAbstractFactory

from command_classes.commands import StartCommand
from command_classes.commands import ResumeCommand
from command_classes.commands import PauseCommand
from command_classes.commands import StopCommand

from utils.command_enums import InputType


class LogCommandFactory(CommandAbstractFactory):

    def __init__(self, command_dict: dict):
        self.command = command_dict['command']
        self.command_time = command_dict['command_args'].time
        self.project_name = command_dict['command_args'].name
        self.log_note = command_dict['command_args'].log_note
        self.session_note = command_dict['command_args'].session_note

    def create_command(self):
        if self.command == InputType.START:
            return self._create_start_command()
        else:
            return self._create_log_command()

    def _create_start_command(self):
        return StartCommand(self.command, self.project_name, self.command_time,
                            self.log_note, self.session_note)

    def _create_log_command(self):
        if self.command == InputType.RESUME:
            return ResumeCommand(self.command, self.command_time, self.log_note)
        elif self.command == InputType.PAUSE:
            return PauseCommand(self.command, self.command_time, self.log_note)
        elif self.command == InputType.STOP:
            return StopCommand(self.command, self.command_time, self.log_note)
