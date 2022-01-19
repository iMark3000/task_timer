from abc import ABC, abstractmethod


class CommandAbstractFactory(ABC):

    @abstractmethod
    def create_command(self):
        pass
