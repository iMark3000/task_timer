from .command_handler_base_class import Handler

from command_classes.commands import QueryCommand
from timer_database.dbManager import DbQueryReport

class QueryCommandHandler(Handler):

    def __init__(self, command: QueryCommand):
        self.command = command
        super().__init__(command)

    def _chronological_report(self):
        pass

    def _report_all_time(self):


    def handle(self):
        if self.command.is_chron:
            self._chronological_report()
