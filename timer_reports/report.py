from typing import List, Tuple
from datetime import datetime
from math import floor

from .report_tree.report_tree import ReportTree
from .report_tree.report_nodes import RootNode
from .report_tree.report_nodes import LogNode
from .report_tree.report_nodes import ProjectNode
from timer_reports.layout_and_print.report_configuration import ROW_FIELD_LAYOUTS
from timer_reports.layout_and_print.report_configuration import SECTION_FOOTER_FIELD_LAYOUTS
from timer_reports.layout_and_print.report_configuration import REPORT_FOOTER_FIELD_LAYOUTS


class ReportPrep:

    def __init__(self, report_level: int, dates: Tuple[str], project_ids: Tuple[str], query_data: List[dict]):
        self.report_level = report_level
        self.project_ids = project_ids
        self.project_names = None
        self.report_dates = dates[0] + " to " + dates[1]
        self.query_data = query_data

    def _set_report_name(self):
        """Setting names for Root Node"""
        name_list = list()
        if len(self.project_ids) < 3:
            for d in self.query_data:
                if d["project_name"] not in name_list:
                    name_list.append(d["project_name"])
                    if len(name_list) == 2:
                        self.project_names = ' & '.join(name_list)
                        break
            if len(name_list) < 2:
                self.project_names = name_list[0]
        else:
            self.project_names = 'MULTIPLE PROJECTS'

    def _convert_times_to_datetime(self):
        """Calculates Durations for LogNodes"""
        for d in self.query_data:
            d['start_time'] = self._convert_to_datetime(self._handle_microseconds(d['start_time']))
            d['end_time'] = self._convert_to_datetime(self._handle_microseconds(d['end_time']))

    def _calculate_durations(self):
        """Calculates Durations for LogNodes"""
        for d in self.query_data:
            d['duration'] = d['end_time'] - d['start_time']

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
        self._set_report_name()
        self._convert_times_to_datetime()
        self._calculate_durations()

    def export_data_for_tree(self):
        export = {
            "reporting_on": self.project_names,
            "reporting_period": self.report_dates,
            "report_data_for_tree": self.query_data,
        }
        return export

    def get_report_level(self):
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


class ReportConstructor:

    def __init__(self, tree: ReportTree, report_type: int, row_node, section_nodes=None):
        self.tree = tree
        self.report_type = report_type
        self.row_node = row_node
        self.section_nodes = section_nodes
        self.row_fields = None
        self.section_fields = None
        self.report_footer_fields = None

    def _get_fields(self):
        self.row_fields = ROW_FIELD_LAYOUTS[self.report_type]
        self.section_fields = SECTION_FOOTER_FIELD_LAYOUTS[self.report_type]
        self.report_footer_fields = REPORT_FOOTER_FIELD_LAYOUTS[self.report_type]

    def _traverse_tree(self, node):
        self._analyze_node(node)
        if hasattr(node, 'children'):
            for child in node.children:
                self._analyze_node(child)

    def _analyze_node(self, node):
        if type(node) == self.row_node:
            row = Row(node, self.row_fields)
        if type(node) in self.section_nodes:
            pass
        elif isinstance(node, RootNode):
            pass

    def construct(self):
        self._get_fields()
        self.traverse_tree()


class Row:

    def __init__(self, node, fields):
        self.node = node
        self.fields = fields
        self._row = dict()

    def compile_row(self):
        for field in self.fields:
            if hasattr(self.node, f'_{field}'):
                self._row[field] = getattr(self.node, f'_{field}')
            elif 'count' in field:
                self._row[field] = len(self.node.children)
            elif 'percent' in field:
                whole_node_type = field.split('_')[1]
                self._row[field] = percent_helper(self.node, whole_node_type)

    @property
    def row(self):
        return self._row


class Section:

    def __init__(self, node, fields):
        self.node = node
        self.fields = fields
        self._header = dict()
        self._footer = dict()

    def compile_header(self):
        if isinstance(self.node, ProjectNode):
            pass


    def compile_footer(self):
        for field in self.fields:
            if hasattr(self.node, f'_{field}'):
                self._footer[field] = getattr(self.node, f'_{field}')
            elif 'count' in field:
                self._footer[field] = len(self.node.children)
            elif 'percent' in field:
                whole_node_type = field.split('_')[1]
                self._footer[field] = percent_helper(self.node, whole_node_type)



class ReportHeaderFooter:
    pass


def average_helper(node):
    t = node.duration
    c = len(node.parent.children)
    return t/c


def percent_helper(node, whole_node_type):
    node_duration = node.duration
    parent = node.parent
    if type(parent) == whole_node_type:
        whole_duration = parent.durantion
    else:
        whole_duration = parent.parent.duration
    return floor(node_duration/whole_duration)


class ReportPrintQueue:
    pass
