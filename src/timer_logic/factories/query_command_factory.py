
from .command_factory_base_class import CommandAbstractFactory
from ...command_classes.query_commands import QueryCommand
from src.utils.command_enums import InputType

# Todo: Make Commands for Query


class QueryCommandFactory(CommandAbstractFactory):

    def __init__(self, command: InputType, command_args: dict):
        self.command = command
        self.command_args = command_args

    def create_command(self):
        return QueryCommand(self.command, **self.command_args)
