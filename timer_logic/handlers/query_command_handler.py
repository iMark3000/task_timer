from .command_handler_base_class import Handler


class QueryCommandHandler(Handler):

    def __init__(self, command: QueryCommand):
        super().__init__(command)

    def handle(self):
        pass
