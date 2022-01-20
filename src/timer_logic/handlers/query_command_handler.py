from typing import List
from datetime import date
from datetime import timedelta

from .command_handler_base_class import Handler
from src.command_classes.commands import QueryCommand
from src.timer_database.dbManager import DbQueryReport

QUERY_TIME_PERIOD_MAP = {
    "W": 7,
    "M": 30,
    "Y": 365
    }

class QueryCommandHandler(Handler):

    def __init__(self, command: QueryCommand):
        self.command = command
        self.projects = dict()
        self.sessions = dict()
        self.db_query = DbQueryReport()

    def _query_for_project_names(self):
        """Checks for project ids; if no project ids, query dates first"""
        pass

    def _query_for_sessions(self):
        """Checks for project ids; if no project ids, query dates first"""
        pass

    def _query_for_logs(self):
        pass

    def _create_time_stamps_for_query_time_period(self) -> dict:
        end_date = date.today()
        if self.command.query_time_period == 'CY':
            year = end_date.year
            start_date = date(year=year, month=1, day=1)
            return {"start": start_date, "end": end_date}
        elif self.command.query_time_period == 'AT':
            return {"end": end_date}
        else:
            days = QUERY_TIME_PERIOD_MAP[self.command.query_time_period] * -1
            td = timedelta(days=days)
            start_date = end_date + td
            return {"start": start_date, "end": end_date}

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

    def _process_queries_top_down(self, project_ids, q_dates):
        pass

    def _process_queries_bottom_up(self, q_dates):
        pass

    def handle(self):
        print(self.command)
        dates = dict()
        # Check for both start and end dates
        if self.command.start_date and self.command.end_date is None:
            dates.update(self._create_time_stamps_for_query_time_period())
        else:
            if self.command.start_date:
                dates["start"] = self.command.start_date
            if self.command.end_date:
                dates["end"] = self.command.end_date

        #check if project IDS exist;
        if
        #   if so, query for ids and work top to bottom
        #   if no ids, query logs and run bottom up
