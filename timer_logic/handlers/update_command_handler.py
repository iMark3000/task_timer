from .command_handler_base_class import Handler


class UpdateCommandHandler(Handler):

    def __init__(self, command: UpdateCommand):
        super().__init__(command)

    def handle(self):
        pass
