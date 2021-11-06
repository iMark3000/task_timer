from abc import ABC, abstractmethod

from utils.command_enums import InputType


class CommandArgParser(ABC):

    def __init__(self, command: InputType, command_args: list):
        self.command = command
        self.command_args = command_args

        @abstractmethod
        def parse():
            pass
