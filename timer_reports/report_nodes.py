

class RootNode:

    def __init__(self):
        self._children = list()
        self._startTime = None
        self._endTime = None
        self._duration = None

    def add_duration(self, duration):
        if self._duration is None:
            self._duration = duration
        else:
            self._duration += duration

    def compare_start_time(self, time):
        if self._startTime is None:
            self._startTime = time
        elif self._startTime > time:
            self._startTime = time

    def compare_end_time(self, time):
        if self._endTime is None:
            self._endTime = time
        elif self._endTime < time:
            self._endTime = time

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
        self._startTime = None
        self._endTime = None
        self._duration = None

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

    @property
    def duration(self):
        return self._duration

    def add_duration(self, duration):
        if self._duration is None:
            self._duration = duration
        else:
            self._duration += duration

    def compare_start_time(self, time):
        if self._startTime is None:
            self._startTime = time
        elif self._startTime > time:
            self._startTime = time

    def compare_end_time(self, time):
        if self._endTime is None:
            self._endTime = time
        elif self._endTime < time:
            self._endTime = time


class ProjectNode(InnerNode):

    def __init__(self, project, project_id):
        self._project = project
        self._project_id = project_id
        super().__init__()

    @property
    def project(self):
        return self._project

    @property
    def project_id(self):
        return self._project_id


class SessionNode(InnerNode):

    def __init__(self, session):
        self._session = session
        super().__init__()

    @property
    def session(self):
        return self._session


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class LogNode:

    def __init__(self, **kwargs):
        self._parent = None
        self._project: None
        self._project_id: None
        self._session: None
        self._logID = None
        self._startTime = None
        self._endTime = None
        self._duration = None
        self._startLogNote = None
        self._endLogNote = None

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
    def project(self):
        return self._project

    @property
    def project_id(self):
        return self._project_id

    @property
    def session(self):
        return self._session

    @property
    def logID(self):
        return self._logID

    @property
    def startTime(self):
        return self._startTime

    @property
    def endTime(self):
        return self._endTime

    @property
    def duration(self):
        return self._duration

    @property
    def startLogNote(self):
        return self._startLogNote

    @property
    def endLogNote(self):
        return self._endLogNote
