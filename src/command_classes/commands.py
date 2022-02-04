from abc import ABC
from typing import Union

from src.utils.command_enums import InputType


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


# ~~~~~~~~~~~QUERY COMMAND FAMILY~~~~~~~~~~~~~~~~~~~~
# Query commands query the database via the query module

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


# ~~~~~~~~~~~CONFIG COMMAND FAMILY~~~~~~~~~~~~~~~~~~~~
# This command did not feel like it fell under any of the
# other groups

class ConfigCommand(Command):

    def __init__(self, command: InputType, **kwargs):
        self._view = None
        self._config_toggle = None
        super().__init__(command, **kwargs)

    def is_view(self):
        return self._view

    def toggle(self) -> Union[str, None]:
        return self._config_toggle
