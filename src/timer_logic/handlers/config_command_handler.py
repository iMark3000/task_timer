from .command_handler_base_class import Handler
from ...command_classes.config_commands import ConfigCommand

from src.config.config_manager import ConfigUpdater


class ConfigCommandHandler(Handler):

    def handle(self, command: ConfigCommand):
        if command.is_view():
            ConfigUpdater().view()
        elif command.toggle() is not None:
            ConfigUpdater().toggle_param(command.toggle())
