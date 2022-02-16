import sys

from typing import List, Tuple
from datetime import date
from datetime import timedelta

from .command_handler_base_class import Handler
from ...command_classes.query_commands import QueryCommand
from src.timer_database.dbManager import DbQueryReport
from src.timer_database.dbManager import log_query_creator

from src.timer_reports.report import create_report

QUERY_TIME_PERIOD_MAP = {
    "W": 7,
    "M": 30,
    "Y": 365
    }


class QueryCommandHandler(Handler):

    def __init__(self):
        self.db_query = DbQueryReport()

    @staticmethod
    def _create_time_stamps_for_query_time_period(command: QueryCommand) -> dict:
        end_date = date.today()
        if command.query_time_period == 'CY':
            year = end_date.year
            start_date = date(year=year, month=1, day=1)
            return {"start_date": start_date, "end_date": end_date}
        elif command.query_time_period == 'AT':
            return {"end_date": end_date, "start_date": None}
        else:
            days = QUERY_TIME_PERIOD_MAP[command.query_time_period] * -1
            td = timedelta(days=days)
            start_date = end_date + td
            return {"start_date": start_date, "end_date": end_date}

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

    def _process_queries_top_down(self, project_ids: Tuple[int], q_dates: dict):
        projects = self.db_query.query_for_project_name(project_ids)
        sessions = self.db_query.query_sessions_by_project_id(project_ids)
        q_dates["session_ids"] = [x["session_id"] for x in sessions]
        log_query_data = log_query_creator(**q_dates)
        logs = self.db_query.log_query(**log_query_data)

        query_data = self.combine_queries(projects, sessions)
        query_data = self.combine_queries(logs, query_data)
        return query_data

    def _process_queries_bottom_up(self, q_dates: dict):
        log_query_data = log_query_creator(**q_dates)
        logs = self.db_query.log_query(**log_query_data)
        session_ids = tuple([x["session_id"] for x in logs])
        sessions = self.db_query.query_sessions_by_session_id(session_ids)
        project_ids = tuple([x["project_id"] for x in sessions])
        projects = self.db_query.query_for_project_name(project_ids)

        query_data = self.combine_queries(sessions, logs)
        query_data = self.combine_queries(projects, query_data)
        return query_data

    def handle(self, command: QueryCommand):

        dates = dict()
        # Check for both start and end dates
        if command.start_date is None and command.end_date is None:
            dates.update(self._create_time_stamps_for_query_time_period(command))
        elif command.end_date is None:
            dates["start_date"] = command.start_date
            dates["end_date"] = date.today()
        else:
            dates["start_date"] = command.start_date
            dates["end_date"] = command.end_date

        try:
            if command.query_projects:
                query_results = self._process_queries_top_down(command.query_projects, dates)
            else:
                query_results = self._process_queries_bottom_up(dates)
        except IndexError:
            sys.exit('Query yielded 0 results.')

        report_data = {
            "reporting_level": command.query_level,
            "reporting_period": (dates["start_date"], dates["end_date"]),
            "report_query": query_results
        }

        if len(report_data["report_query"]) != 0:
            create_report(report_data)
