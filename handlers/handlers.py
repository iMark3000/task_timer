from abc import ABC
from .commands import Command


class Handler(ABC):

    def __init__(self, command_obj: Command):
        self.command_obj = command_obj


class LogCommandHandler(Handler):
    pass


class QueryCommandHandler(Handler):
    pass
