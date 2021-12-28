from datetime import timedelta
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

    def __init__(self, node, fields, sub_section=None):
        self._node = node
        self._fields = fields
        self._data = dict()
        self.sub_section = sub_section
        self._count_container = dict()

    def _calculate_fields(self, fields):
        for field in fields:
            if hasattr(self._node, f'_{field}'):
                self._data[field] = getattr(self._node, f'_{field}')
            elif 'count' in field and not isinstance(self._node, LogNode):
                count_node_type = field.split('_')[1]
                self._count_container[count_node_type] = count_and_average_helper(self._node, count_node_type)
                self._data[field] = self._count_container[count_node_type][0]
            elif 'average' in field:
                ave_node_type = field.split('_')[1]
                count, duration = self._count_container[ave_node_type]
                self._data[field] = duration / count
            elif 'percent' in field:
                whole_node_type = field.split('_')[1]
                self._data[field] = percent_helper(self._node, whole_node_type)

    def compile_data(self):
        if 'row_fields' in self._fields.keys():
            self._calculate_fields(self._fields['row_fields'])
        if 'headers' in self._fields.keys():
            self._calculate_fields(self._fields['headers'])
        if 'footers' in self._fields.keys() and not self.sub_section:
            self._calculate_fields(self._fields['footers'])

    @property
    def data(self):
        return self._data

    def is_sub_section(self):
        return self.sub_section


class Row(ReportComponent):

    def __init__(self, node, fields):
        super().__init__(node, fields)


class Section(ReportComponent):

    def __init__(self, node, fields, sub_section=None):
        super().__init__(node, fields, sub_section)


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


def count_and_average_helper(node, count_node_type, count=0, duration=None):
    if duration is None:
        duration = timedelta(0)
    node_type = NODE_LOOKUP[count_node_type]
    for child in node.children:
        if type(child) == node_type:
            count += 1
            duration += child.duration
        else:
            if type(child) != LogNode:
                if len(child.children) != 0:
                    return count_and_average_helper(child, count_node_type, count=count, duration=duration)
                else:
                    pass
    return count, duration


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
