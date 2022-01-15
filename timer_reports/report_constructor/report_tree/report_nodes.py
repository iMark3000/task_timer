from datetime import timedelta


class RootNode:

    def __init__(self, reporting_on: str, reporting_period: str):
        self.reporting_on = reporting_on
        self.reporting_period = reporting_period
        self._children = list()
        self._duration = timedelta(0)

    def add_child(self, node):
        node.parent = self
        self._children.append(node)

    @property
    def children(self):
        return self._children

    @property
    def duration(self):
        return self._duration

    def add_to_duration(self, d):
        self._duration += d

    def __str__(self):
        return f'{self.reporting_on}'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class InnerNode:

    def __init__(self):
        self._parent = None
        self._children = list()
        self._duration = timedelta(0)

    def add_child(self, node):
        node.parent = self
        self._children.append(node)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, p):
        self._parent = p

    @property
    def children(self):
        return self._children

    @property
    def duration(self):
        return self._duration

    def add_to_duration(self, d):
        self._duration += d


class ProjectNode(InnerNode):

    def __init__(self, project_name, project_id):
        self._project_name = project_name
        self._project_id = project_id
        super().__init__()

    @property
    def project_name(self):
        return self._project_name

    @property
    def project_id(self):
        return self._project_id

    @property
    def session_count(self):
        return len(self.children)

    def __str__(self):
        return f'{self.project_name} {self.project_id}'


class SessionNode(InnerNode):

    def __init__(self, session_id, session_note=None):
        self._session_id = session_id
        self._session_note = session_note
        super().__init__()

    @property
    def session_id(self):
        return self._session_id

    @property
    def session_note(self):
        return self._session_note

    @property
    def log_count(self):
        return len(self.children)

    def __str__(self):
        return f'Session: {self.session_id}'


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class LogNode:

    def __init__(self, **kwargs):
        self._parent = None
        self._project_name = None
        self._project_id = None
        self._session_id = None
        self._log_id = None
        self._start_time = None
        self._end_time = None
        self._duration = None
        self._start_log_note = None
        self._end_log_note = None

        for key, value in kwargs.items():
            if f'_{key}' in self.__dict__.keys():
                self.__dict__[f'_{key}'] = value

    @property
    def project_name(self):
        return self._project_name

    @property
    def project_id(self):
        return self._project_id

    @property
    def session_id(self):
        return self._session_id

    @property
    def log_id(self):
        return self._log_id

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def duration(self):
        return self._duration

    @property
    def start_log_note(self):
        return self._start_log_note

    @property
    def end_log_note(self):
        return self._end_log_note

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, p):
        self._parent = p

    def __str__(self):
        return f'LOG: {self.log_id}'
