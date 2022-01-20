from typing import List, Tuple
from datetime import datetime
from datetime import timedelta

from src.timer_reports.report_constructor.report_tree.report_tree import ReportTree

from src.timer_reports.report_constructor.report_tree.report_nodes import RootNode
from src.timer_reports.report_constructor.report_tree.report_nodes import ProjectNode
from src.timer_reports.report_constructor.report_tree.report_nodes import SessionNode
from src.timer_reports.report_constructor.report_tree.report_nodes import LogNode

from src.timer_reports.layout.layout_manager import LayoutManager

from src.timer_reports.report_constructor.report_componenets import Section
from src.timer_reports.report_constructor.report_componenets import Row
from src.timer_reports.report_constructor.report_componenets import ReportHeaderSummary


class ReportPrep:

    def __init__(self, dates: Tuple[datetime, datetime], query_data: List[dict]):
        self.project_names = None
        self.report_dates = dates
        self.query_data = query_data

    def _set_report_name(self):
        """Setting names and time period for Report"""
        name_set = set()
        for d in self.query_data:
            name_set.add(d["project_name"])

        if len(name_set) <= 2:
            name_set = list(name_set)
            self.project_names = f'{name_set[0]} and {name_set[1]}'
        else:
            self.project_names = 'MULTIPLE PROJECTS'

    def _convert_times_to_datetime(self):
        """Converts start and end dates to datetime objects"""
        for d in self.query_data:
            d['start_timestamp'] = self._convert_to_datetime(self._handle_microseconds(d['start_timestamp']))
            d['end_timestamp'] = self._convert_to_datetime(self._handle_microseconds(d['end_timestamp']))

    def _calculate_durations(self):
        """Calculates durations for each line of data"""
        for d in self.query_data:
            d['duration'] = d['end_timestamp'] - d['start_timestamp']

    @staticmethod
    def _handle_microseconds(tstamp):
        """Removes millisecondsself.project_ids from time strings so duration can be calculated"""
        # Todo: Make better; Can timestamps w/o milliseconds have milliseconds added?
        if '.' in tstamp:
            return tstamp.split('.')[0]
        else:
            return tstamp

    @staticmethod
    def _convert_to_datetime(time):
        _format = "%Y-%m-%d %H:%M:%S"
        return datetime.strptime(time, _format)

    def _create_report_date_string(self):
        _format = "%Y-%m-%d"
        return f'{datetime.strftime(self.report_dates[0], _format)} to ' \
               f'{datetime.strftime(self.report_dates[1], _format)}'

    def prep_report(self):
        """Driver method"""
        self._set_report_name()
        self._convert_times_to_datetime()
        self._calculate_durations()

    def export_data_for_tree(self):
        """Getter for data to be fed to ReportTree"""
        export = {
            "reporting_on": self.project_names,
            "reporting_period": self._create_report_date_string(),
            "report_data_for_tree": self.query_data,
        }
        return export


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


class ReportConstructor:

    def __init__(self, tree: ReportTree, report_layout: LayoutManager):
        self.tree = tree
        self.row_node = report_layout.report_row
        self.section_nodes = report_layout.report_sections
        self.row_fields = report_layout.report_row_fields
        self.section_fields = report_layout.report_section_fields
        self.report_header_footer_fields = report_layout.report_header_footer_fields
        self._component_container = list()

    def _traverse_tree(self, node):
        self._analyze_node(node)
        if hasattr(node, 'children'):
            for child in node.children:
                self._traverse_tree(child)

    def _analyze_node(self, node):
        if type(node) == self.row_node:
            self._component_container.append(Row(node, self.row_fields))
        if type(node) in self.section_nodes:
            if type(node) == self.section_nodes[0]:
                # First node in the list is the primary section
                self._component_container.append(Section(node, self.section_fields))
            else:
                self._component_container.append(Section(node, self.section_fields, sub_section=True))
        elif isinstance(node, RootNode):
            self._component_container.append(ReportHeaderSummary(node, self.report_header_footer_fields))

    def construct(self):
        self._traverse_tree(self.tree.root)

    def get_report_components(self):
        return self._component_container


def total_duration_helper(tree: ReportTree):
    """Entry point to traverse tree and sum durations"""
    node_types = [SessionNode, ProjectNode, RootNode]
    for node_type in node_types:
        _total_duration_traversal(node_type, tree.root)


def _total_duration_traversal(node_type, node):
    """Traverses tree and sums duration based on the type of Node being passed"""
    if isinstance(node, node_type):
        for child in node.children:
            node.add_to_duration(child.duration)
    else:
        if hasattr(node, 'children'):
            for child in node.children:
                _total_duration_traversal(node_type, child)