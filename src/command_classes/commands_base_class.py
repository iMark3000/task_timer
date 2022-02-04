from abc import ABC

from src.utils.command_enums import InputType


class CommandBaseClass(ABC):
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
