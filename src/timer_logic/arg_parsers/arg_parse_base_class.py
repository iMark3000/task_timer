from abc import ABC, abstractmethod

from src.utils.command_enums import InputType


class CommandArgParser(ABC):

    def __init__(self, command: InputType, command_args: list):
        self.command = command
        self.command_args = command_args
        self.arg_dict = dict()

    def get_command_tuple(self):
        return self.command, self.arg_dict

    @abstractmethod
    def parse(self):
        pass
