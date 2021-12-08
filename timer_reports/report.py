from typing import List, Tuple
from datetime import datetime

from .report_tree.report_tree import ReportTree
from .report_tree.report_nodes import RootNode
from .report_tree.report_nodes import LogNode


class Report:
    """Container for all of the parts needed to put together a report"""
    def __init__(self):
        self.report_constrtutor = None
        self.report_tree = None
        self.report_formats = None
        self.report_print_queue = None


class ReportConstructor:

    def __init__(self, report_level: int, dates: Tuple[str], project_ids: List[str], query_data: List[dict]):
        self.report_level = report_level
        self.project_ids = project_ids
        self.project_names = None
        self.report_dates = dates[0] + " to " + dates[1]
        self.query_data = query_data

    def _set_names(self):
        """Setting names for Root Node"""
        name_list = list()
        if len(self.project_ids) < 3:
            for d in self.query_data:
                if d["project"] not in name_list:
                    name_list.append(d["project"])
                    if len(name_list) == 2:
                        break
            self.project_names = ' & '.join(name_list)
        else:
            self.project_names = 'MULTIPLE PROJECTS'

    def _get_durations(self):
        """Calculates Durations for LogNodes"""
        for d in self.query_data:
            d['startTime'] = self._handle_microseconds(d['startTime'])
            d['endTime'] = self._handle_microseconds(d['endTime'])
            d['duration'] = self._convert_to_datetime(d['endTime']) - self._convert_to_datetime(d['startTime'])
        self.query_data.sort(key=lambda x: (x['project_id'], x['session'], x['logID']))

    @staticmethod
    def _handle_microseconds(tstamp):
        """Removes milliseconds from time strings so duration can be calculated"""
        # Todo: Make better; Can timestamps w/o milliseconds have milliseconds added?
        if '.' in tstamp:
            return tstamp.split('.')[0]
        else:
            return tstamp

    @staticmethod
    def _convert_to_datetime(time):
        _format = "%Y-%m-%d %H:%M:%S"
        return datetime.strptime(time, _format)

    def prep_report(self):
        self._set_names()
        self._get_durations()

    def export_data_for_tree(self):
        export = {
            "reporting_on": self.project_names,
            "reporting_period": self.report_dates,
            "report_data_for_tree": self.query_data,
        }
        return export

    def get_report_leve(self):
        return self.report_level


class ReportTreeCreator:

    def __init__(self, **kwargs):
        self.tree = ReportTree()
        self.reporting_on = None
        self.reporting_period = None
        self.report_data_for_tree = None
        for key, value in kwargs.items():
            if key in self.__dict__.keys():
                self.__dict__[key] = value

    def _create_root(self):
        root = RootNode(self.reporting_on, self.reporting_period)
        self.tree.root = root

    @staticmethod
    def _create_log_node(data):
        return LogNode(**data)

    def build_tree(self):
        self._create_root()
        for line in self.report_data_for_tree:
            node = self._create_log_node(line)
            self.tree.add_node(self.tree.root, node)

    def get_tree(self):
        return self.tree
