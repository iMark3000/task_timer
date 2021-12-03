
from report_nodes import RootNode
from report_nodes import ProjectNode
from report_nodes import SessionNode
from report_nodes import LogNode


class ReportTree:

    def __init__(self):
        self._root = None

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, node: RootNode):
        self._root = node

    def add_node(self, parent, node: LogNode):
        self._visit_inner_node(parent, node)
        if isinstance(parent, RootNode):
            project = [x for x in parent.children() if x.project_id == node.project_id]
            if len(project) == 0:
                self._add_project_node(node)
            else:
                project = project[0]
                self.add_node(project, node)
        elif isinstance(parent, ProjectNode):
            session = [x for x in parent.children() if x.session == node.session]
            if len(session) == 0:
                self._add_session_node(parent, node)
            else:
                session = session[0]
                self._visit_inner_node(session, node)
                session.add_child(node)

    @staticmethod
    def _visit_inner_node(inner_node, node):
        inner_node.compare_start_time(node.startTime)
        inner_node.compare_end_time(node.endTime)
        inner_node.add_duration(node.duration)

    def _add_project_node(self, node: LogNode):
        new_node = ProjectNode(node.project, node.project_id)
        self.root.add_child(new_node)
        self._visit_inner_node(new_node, node)
        self._add_session_node(new_node, node)

    def _add_session_node(self, parent: ProjectNode, node: LogNode):
        new_node = SessionNode(node.session)
        parent.add_child(new_node)
        self._visit_inner_node(new_node, node)
        new_node.add_child(node)


"""
class ReportSummary:

    def __init__(self):
        self.total_duration = None
        self.project_count = set()
        self.session_count = set()
        self.log_count = 0
        self.report_timeperiod = None

    def tabulate_row(self, row):
        self._add_project(row['project_id'])
        self._add_session(row['session'])

    def _add_project(self, project_id):
        self.project_count.add(project_id)

    def _add_session(self, session):
        self.project_count.add(session)

    def _add_duration(self, duration):
        if self.total_duration is None:
            self.total_duration = duration
        else:
            self.total_duration += duration


class ReportQueue:

    def __init__(self, size=None):
        self._start_index = 0
        self._end_index = 0
        if size:
            self._data = [None] * size
        else:
            self._data = [None] * 10

    def enqueue(self, line):
        self._data[self._end_index] = line
        self._end_index += 1

    def view_top_attr(self, key):
        return self._data[self._start_index][key]

    def dequeue(self):
        line = self._data[self._start_index]
        self._data[self._start_index] = None
        self._start_index += 1

    def is_empty(self):
        return self._start_index == self._end_index


class ReportQueuePrint:

    def __init__(self, formatter, report_level):
        pass

    def print_header(self):
        pass

    def print_column_headers(self):
        pass

    def print_row(self):
        pass

    def print_summary(self):
        pass


class ReportContainer:

    def __init__(self):
        self.project_reports = dict()
        self.session_reports = dict()
        self.summary = dict()

    def add_row(self, row):
        if row['project_id'] not in self.project_reports:
            new_project = ProjectReport(row['project'], row['project_id'])
            new_project.add_row_to_session(row)
            self.project_reports[row['project_id']] = new_project
        else:
            self.project_reports[row['project_id']].add_row_to_session(row)

    def get_projects(self):
        return list(self.project_reports.values())

    def get_project_summary(self, project_id):
        return self.project_reports[project_id].summary

    def get_project_sessions(self, project):
        return self.project_reports[project_id].summary.get_sessions()


class ProjectReport:

    def __init__(self, name, pid):
        self._name = name
        self._project_id = pid
        self.session_obj = dict()
        self.summary = dict()

    def add_row_to_session(self, data):
        if data['session'] in self.session_obj.keys():
            self.session_obj[data['session']].add_log(data)
        else:
            new_session = SessionReport(data['session'])
            new_session.add_log(data)
            self.session_obj[data['session']] = new_session

    @property
    def project_name(self):
        return self._name

    @property
    def project_id(self):
        return self._project_id

    def get_sessions(self):
        return list(self.session_obj.values())

    def count_of_sessions(self):
        return len(self.session_obj)

    def add_to_summary(self, k, v):
        self.summary[k] = v



class SessionReport:

    def __init__(self, sid):
        self._session_id = sid
        self.logs = list()
        self.summary = dict()

    def add_log(self, log_data):
        new_entry = dict()
        new_entry['logID'] = log_data['logID']
        new_entry['startTime'] = self.handle_microseconds(log_data['startTime'])
        new_entry['endTime'] = self.handle_microseconds(log_data['endTime'])
        new_entry['duration'] = self.calculate_duration(new_entry)
        new_entry['startLogNote'] = log_data['startLogNote']
        new_entry['endLogNote'] = log_data['endLogNote']
        self.logs.append(new_entry)

    def calculate_duration(self, data):
        format = "%Y-%m-%d %H:%M:%S"
        return datetime.strptime(data['endTime'], format) - datetime.strptime(data['startTime'], format)

    def handle_microseconds(self, tstamp):
        # Todo: Make better
        if '.' in tstamp:
            return tstamp.split('.')[0]
        else:
            return tstamp

    @property
    def session_id(self):
        return self._session_id

    def get_logs(self):
        return self.logs

    def count_of_logs(self):
        return len(self.logs)

    def add_to_summary(self, k, v):
        self.summary[k] = v
"""
