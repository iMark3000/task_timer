from .command_handler_base_class import Handler
from ...command_classes.config_commands import ConfigCommand

from src.config.config_manager import ConfigUpdater
from src.utils.exceptions import InvalidConfigArgument


class ConfigCommandHandler(Handler):

    def __init__(self, command: ConfigCommand):
        self.command = command

    def handle(self):
        if self.command.is_view():
            ConfigUpdater().view()
        elif self.command.toggle() is not None:
            ConfigUpdater().toggle_param(self.command.toggle())
