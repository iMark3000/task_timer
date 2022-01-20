from typing import List, Tuple
from datetime import date
from datetime import timedelta

from .command_handler_base_class import Handler
from src.command_classes.commands import QueryCommand
from src.timer_database.dbManager import DbQueryReport
from src.timer_database.dbManager import log_query_creator

from src.timer_reports.report import create_report

QUERY_TIME_PERIOD_MAP = {
    "W": 7,
    "M": 30,
    "Y": 365
    }


class QueryCommandHandler(Handler):

    def __init__(self, command: QueryCommand):
        self.command = command
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
            return {"start_date": start_date, "end_date": end_date}
        elif self.command.query_time_period == 'AT':
            return {"end_date": end_date}
        else:
            days = QUERY_TIME_PERIOD_MAP[self.command.query_time_period] * -1
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

    def handle(self):
        print(self.command)
        dates = dict()
        # Check for both start and end dates
        if self.command.start_date and self.command.end_date is None:
            dates.update(self._create_time_stamps_for_query_time_period())
        else:
            if self.command.start_date:
                dates["start_date"] = self.command.start_date
            if self.command.end_date:
                dates["end_date"] = self.command.end_date

        if self.command.query_projects:
            query_results = self._process_queries_top_down(self.command.query_projects, dates)
        else:
            query_results = self._process_queries_bottom_up(dates)

        # TODO: reporting_on is gone....check that this doesn't create bugs
        # TODO: reporting_period is a tuple of date objects; not strings. This will need to be fixed in ReportPrep
        report_data = {
            "reporting_level": self.command.query_level,
            "reporting_period": (self.command.start_date, self.command.end_date),
            "report_query": query_results
        }

        create_report(report_data)
