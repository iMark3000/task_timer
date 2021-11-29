
from .command_factory_base_class import CommandAbstractFactory
from command_classes.commands import QueryCommand

# Todo: Make Commands for Query
from command_classes.commands import *


class QueryCommandFactory(CommandAbstractFactory):

    def __init__(self, command_dict: dict):
        self.command = command_dict['command']

    def create_command(self):
        return QueryCommand(self.command, **self.command_args)
