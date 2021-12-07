

class RootNode:

    def __init__(self):
        self._children = list()

    def add_child(self, node):
        node.parent = self
        self._children.append(node)

    @property
    def children(self):
        return self._children

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class InnerNode:

    def __init__(self):
        self._parent = None
        self._children = list()

    def __getattr__(self, item):
        if item in self.__dict__.keys():
            return self.__dict__[item]

    def add_child(self, node):
        node.parent = self
        self._children.append(node)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, node):
        self._parent = node

    @property
    def children(self):
        return self._children


class ProjectNode(InnerNode):

    def __init__(self, project_name, project_id):
        self._project_name = project_name
        self._project_id = project_id
        super().__init__()

    @property
    def project(self):
        return self._project_name

    @property
    def project_id(self):
        return self._project_id

    @property
    def session_count(self):
        return len(self.children)

class SessionNode(InnerNode):

    def __init__(self, session, session_note=None):
        self._session = session
        self._session_note = session_note
        super().__init__()

    @property
    def session(self):
        return self._session

    @property
    def session_note(self):
        return self._session_note

    @property
    def log_count(self):
        return len(self.children)

    @property
    def session_duration(self):
        duration = 0
        for c in self.children:
            duration += c.duration
        return duration


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class LogNode:

    def __init__(self, **kwargs):
        self._parent = None
        self._project_name: None
        self._project_id: None
        self._session: None
        self._log_id = None
        self._start_time = None
        self._end_time = None
        self._duration = None
        self._start_log_note = None
        self._end_log_note = None

        for key, value in kwargs.items():
            if key in self.__dict__.keys():
                self.__dict__[key] = value

    def __getattr__(self, item):
        if item in self.__dict__.keys():
            return self.__dict__[item]

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def set_parent(self, node: InnerNode):
        self._parent = node

    @property
    def project_name(self):
        return self._project_name

    @property
    def project_id(self):
        return self._project_id

    @property
    def session(self):
        return self._session

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
    def session_percentage(self):
        return self.duration / self.parent.get_duration()

