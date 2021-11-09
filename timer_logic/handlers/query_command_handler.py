from .command_handler_base_class import Handler

from command_classes.commands import QueryCommand

class QueryCommandHandler(Handler):

    def __init__(self, command: QueryCommand):
        super().__init__(command)

    def handle(self):
        pass
