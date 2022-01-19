import datetime

from .command_handler_base_class import Handler
from command_classes.commands import QueryCommand
from timer_database.dbManager import DbQueryReport


class QueryCommandHandler(Handler):

    def __init__(self, command: QueryCommand):
        self.command = command
        super().__init__(command)

    def _check_for_dates(self):
        """Checks command args for dates"""
        pass

    def _check_for_time_period(self):
        """Checks for time period if dates do not exist"""
        pass

    def _check_for_project_ids(self):
        """Checks for project ids; if no project ids, query dates first"""
        pass

    def handle(self):
        print(self.command)
