from typing import Union

from timer_reports.report_constructor.report_tree.report_nodes import RootNode
from timer_reports.report_constructor.report_tree.report_nodes import ProjectNode
from timer_reports.report_constructor.report_tree.report_nodes import SessionNode
from timer_reports.report_constructor.report_tree.report_nodes import LogNode

NODE_LOOKUP = {
    'LogNode': LogNode,
    'SessionNode': SessionNode,
    'ProjectNode': ProjectNode,
    'RootNode': RootNode
}


class ReportComponent:

    def __init__(self, node, fields, sub_section=False):
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
                self._count_container[count_node_type] = count_helper(self._node, count_node_type)
                self._data[field] = self._count_container[count_node_type][0]
            elif 'average' in field:
                ave_node_type = field.split('_')[1]
                count, duration = self._count_container[ave_node_type]
                print(f'\nNode: {self._node}\nCount: {count} duration: {duration}')
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

    @property
    def node(self) -> Union[RootNode, ProjectNode, SessionNode, LogNode]:
        return self._node

    def __str__(self):
        if isinstance(self.node, LogNode):
            return f'SESSION: {self.node.session_id} - {self.node}'
        elif isinstance(self.node, SessionNode):
            return f'PROJECT: {self.node.parent.project_name} ({self.node.parent.project_id}) - {self.node}'
        elif isinstance(self.node, ProjectNode):
            return f'--- {self.node} --'
        elif isinstance(self.node, RootNode):
            return f'ROOT: {self.node}'


class Row(ReportComponent):

    def __init__(self, node, fields):
        super().__init__(node, fields)


class Section(ReportComponent):

    def __init__(self, node, fields, sub_section=False):
        super().__init__(node, fields, sub_section)


class ReportHeaderSummary(ReportComponent):

    def __init__(self, node, fields):
        super().__init__(node, fields)

    def compile_report_header(self):
        self._data['reporting_on'] = self._node.reporting_on
        self._data['reporting_period'] = self._node.reporting_period


def count_helper(node, count_node_type, count=0):
    print(f'FUNC NODE: {node}')
    node_type = NODE_LOOKUP[count_node_type]
    for child in node.children:
        if type(child) == node_type:
            count += 1
        else:
            if len(child.children) != 0:
                return count_helper(child, count_node_type, count=count)
            else:
                pass
    return count


def total_duration_helper(node, duration=None):
    for child in node.children:
        if isinstance(child, LogNode):
            if duration is None:
                duration = child.duration
            else:
                duration += child.duration
        else:
            total_duration_helper(child, duration=duration)
    return duration


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
