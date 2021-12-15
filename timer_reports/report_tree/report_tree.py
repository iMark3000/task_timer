
from timer_reports.report_tree.report_nodes import RootNode
from timer_reports.report_tree.report_nodes import ProjectNode
from timer_reports.report_tree.report_nodes import SessionNode
from timer_reports.report_tree.report_nodes import LogNode


class ReportTree:

    def __init__(self):
        self._root = None

    @property
    def root(self) -> RootNode:
        return self._root

    @root.setter
    def root(self, node: RootNode):
        self._root = node

    def add_node(self, parent, node: LogNode):
        parent.duration = node.duration
        if isinstance(parent, RootNode):
            project = [x for x in parent.children if x.project_id == node.project_id]
            if len(project) == 0:
                self._add_project_node(node)
            else:
                project = project[0]
                self.add_node(project, node)
        elif isinstance(parent, ProjectNode):
            session = [x for x in parent.children if x.session_id == node.session_id]
            if len(session) == 0:
                self._add_session_node(parent, node)
            else:
                session = session[0]
                session.add_child(node)
                session.dufation = node.duration

    def _add_project_node(self, node: LogNode):
        new_node = ProjectNode(node.project_name, node.project_id)
        new_node.duration = node.duration
        self.root.add_child(new_node)
        self._add_session_node(new_node, node)

    @staticmethod
    def _add_session_node(parent: ProjectNode, node: LogNode):
        new_node = SessionNode(node.session_id)
        new_node.duration = node.duration
        parent.add_child(new_node)
        new_node.add_child(node)
