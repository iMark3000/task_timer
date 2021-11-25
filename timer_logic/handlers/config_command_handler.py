from typing import Union

from .command_handler_base_class import Handler
from timer_database.dbManager import DbUpdate, DbQueryUtility
from command_classes.commands import ConfigCommand

from config.config_manager import ConfigUpdater
from utils.exceptions import InvalidConfigArgument


class ConfigCommandHandler(Handler):

    def __init__(self, command: ConfigCommand):
        self.command = command

    def handle(self):
        if self.command.is_view():
            ConfigUpdater().view()
        else:
            try:
                ConfigUpdater().update(self.command.get_key(), self.command.get_value())
            except(KeyError, InvalidConfigArgument) as e:
                print(e)

