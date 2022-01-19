from typing import List

from .command_handler_base_class import Handler
from src.command_classes.commands import QueryCommand


class QueryCommandHandler(Handler):

    def __init__(self, command: QueryCommand):
        self.command = command
        self.projects = dict()
        self.sessions = dict()

    def _check_for_dates(self):
        """Checks command args for dates"""
        pass

    def _check_for_time_period(self):
        """Checks for time period if dates do not exist"""
        pass

    def _get_project_names(self):
        """Checks for project ids; if no project ids, query dates first"""
        pass

    @staticmethod
    def combine_queries(query1: List[dict], query2: List[dict]) -> List[dict]:
        """Evaluates list of dicts by common key and combines them if values match."""
        combined_list = list()
        key_value = [k for k in list(query1[0].keys()) if k in query2[0].keys()][0]
        for row1 in query1:
            for row2 in query2:
                if row1[key_value] == row2[key_value]:
                    combined_list.append({**row1, **row2})
        return combined_list


    def handle(self):
        print(self.command)
        #
