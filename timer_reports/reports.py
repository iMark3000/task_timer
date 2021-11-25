from datetime import datetime


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
