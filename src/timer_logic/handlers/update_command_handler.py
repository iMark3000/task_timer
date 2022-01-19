from .command_handler_base_class import Handler

from src.command_classes.commands import UpdateCommand


class UpdateCommandHandler(Handler):

    def __init__(self, command: UpdateCommand):
        super().__init__(command)

    def handle(self):
        pass
