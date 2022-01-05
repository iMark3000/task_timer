import datetime

from .command_handler_base_class import Handler
from command_classes.commands import QueryCommand
from timer_database.dbManager import DbQueryReport

class QueryCommandHandler(Handler):

    def __init__(self, command: QueryCommand):
        self.command = command
        super().__init__(command)

    def _report_all_time(self):
        pass

    def _create_query_time_period(self):
        if self.command.query_time_period in ['W', 'M', 'Y', 'CY', 'AT']:
            pass

    def _quick_query_translation(self):


    def handle(self):
