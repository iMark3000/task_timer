from abc import ABC, abstractmethod

from ...command_classes.commands_base_class import CommandBaseClass


class Handler(ABC):

    @abstractmethod
    def handle(self, command: CommandBaseClass):
        pass
