from abc import ABC, abstractmethod

from ..report_tree.report_nodes import RootNode
from ..report_tree.report_nodes import ProjectNode
from ..report_tree.report_nodes import SessionNode
from ..report_tree.report_nodes import LogNode

NODE_LOOKUP = {
    'LogNode': LogNode,
    'SessionNode': SessionNode,
    'ProjectNode': ProjectNode,
    'RootNode': RootNode
}


class ReportComponent:

    def __init__(self, node, fields):
        self._node = node
        self._fields = fields
        self._data = dict()

    def compile_data(self):
        for field in self._fields:
            if hasattr(self._node, f'_{field}'):
                self._data[field] = getattr(self._node, f'_{field}')
            elif 'count' in field and not isinstance(self._node, LogNode):
                count_node_type = field.split('_')[1]
                self._data[field] = count_helper(self._node, count_node_type)
            elif 'average' in field:
                self._data[field] = average_helper(self._node)
            elif 'percent' in field:
                whole_node_type = field.split('_')[1]
                self._data[field] = percent_helper(self._node, whole_node_type)

    @property
    def data(self):
        return self._data


class Row(ReportComponent):

    def __init__(self, node, fields):
        super().__init__(node, fields)


class Section(ReportComponent):

    def __init__(self, node, fields, sub_section=False):
        self.sub_section = sub_section
        super().__init__(node, fields)

    def is_sub_section(self):
        return self.sub_section


class ReportHeaderSummary(ReportComponent):

    def __init__(self, node, fields):
        self._header = dict()
        super().__init__(node, fields)

    def compile_report_header(self):
        self._header['reporting_on'] = self._node.reporting_on
        self._header['reporting_period'] = self._node.reporting_period

    @property
    def header(self):
        return self._header


def average_helper(node):
    t = node.duration
    c = len(node.parent.children)
    return t/c


def count_helper(node, count_node_type, tot=0):
    node_type = NODE_LOOKUP[count_node_type]
    for child in node.children:
        if type(child) == node_type:
            tot += 1
        else:
            if len(child.children) != 0:
                return count_helper(child, count_node_type, tot=tot)
    return tot


def percent_helper(node, whole_node_type):
    node_duration = node.duration
    whole_node_type = NODE_LOOKUP[whole_node_type]
    parent = get_correct_whole_node(node.parent, whole_node_type)
    whole_duration = parent.duration
    return node_duration/whole_duration


def get_correct_whole_node(parent, node_type):
    if type(parent) == node_type:
        return parent
    else:
        return get_correct_whole_node(parent.parent, node_type)
