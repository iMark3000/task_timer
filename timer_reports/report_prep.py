from typing import List, Tuple
from datetime import datetime

from command_classes.commands import QueryCommand
from report_tree import ReportQueue
from report_tree import ReportSummary
from report_tree import ReportQueuePrint


class ReportConstructor:

    def __init__(self, report_level: int, dates: Tuple[str], project_ids: List[str], query_data: List[dict]):
        self.report_level = report_level
        self.start_date = dates[0]
        self.end_date = dates[1]
        self.project_ids = project_ids
        self.project_names = None
        self.query_data = query_data

    def set_names(self):
        name_list = list()
        if len(self.project_ids) < 3:
            for d in self.query_data:
                if d["project"] not in name_list:
                    name_list.append(d["project"])
                    if len(name_list) == 2:
                        break
            self.project_names = ' & '.join(name_list)
        else:
            self.project_names = 'MULTIPLE PROJECTS'

    def process_data(self):
        for d in self.query_data:
            d['startTime'] = self.handle_microseconds(d['startTime'])
            d['endTime'] = self.handle_microseconds(d['endTime'])
            d['duration'] = self.convert_to_datetime(d['endTime']) - self.convert_to_datetime(d['startTime'])
        self.query_data.sort(key=lambda x: (x['project_id'], x['session'], x['logID']))

    @staticmethod
    def handle_microseconds(tstamp):
        # Todo: Make better
        if '.' in tstamp:
            return tstamp.split('.')[0]
        else:
            return tstamp

    @staticmethod
    def convert_to_datetime(time):
        _format = "%Y-%m-%d %H:%M:%S"
        return datetime.strptime(time, _format)

    def set_up_report(self):
        self.set_names()
        self.process_data()


class ReportTemplate:

    def __init__(self, level):
        self.level = level

    @staticmethod
    def _log_level_template(self):
        report_max_width = 165
        footer_fields = (
            'TOTAL DURATION:',
            'COUNT OF PROJECTS:',
            'AVE TIME PER: PROJECT:',
            'COUNT OF SESSIONS:',
            'AVE TIME PER SESSION:',
            "COUNT OF LOGS:",
            "AVE TIME PER LOG:"
        )
        row_headers = (
            "PROJECT",
            "SESSION ID",
            "LOG ID",
            "START",
            "END",
            "DURATION",
            "%REPORT",
            "NOTES"
        )
        row_formats = {
            "LOG ID": {"align": '^', "width": .076},
            "START": {"align": "^", "width": .169},
            "END": {"align": '^', "width": .169},
            "DURATION": {"align": '^', "width": .135},
            "%SESSION": {"align": '^', "width": .118},
            "%PROJECT": {"align": '^', "width": .118},
            "NOTES": {"align": '<'}
        }
        return {'report_max_width': report_max_width, 'footer_fields': footer_fields,
                'row_headers': row_headers,'row_formats': row_formats}

    @staticmethod
    def _session_level_template(self):
        report_max_width = 135
        footer_fields = (
            'TOTAL DURATION:',
            'COUNT OF PROJECTS:',
            'AVE TIME PER: PROJECT:',
            'COUNT OF SESSIONS:',
            'AVE TIME PER SESSION:'
        )
        row_headers = (
            "SESSION ID",
            "DURATION",
            '%PROJECT',
            "NOTES"
        )
        row_formats = {
            "SESSION ID": {"align": '^', "width": 0.135},
            "DURATION": {"align": '^', "width": 0.237},
            "%PROJECT": {"align": '^', "width": 0.16},
            "NOTES": {"align": '<'}
        }
        return {'report_max_width': report_max_width, 'footer_fields': footer_fields,
                'row_headers': row_headers, 'row_formats': row_formats}

    @staticmethod
    def _project_level_template():
        report_max_width = 118
        footer_fields = (
            "TOTAL DURATION",
            "COUNT OF PROJECTS",
            "AVE TIME PER PROJECT",
            "COUNT OF LOGS",
            "AVE TIME PER LOG"
        )
        row_headers = (
            "LOG ID",
            "START",
            "END",
            "DURATION",
            "%%SESSION",
            "%PROJECT",
            "NOTES"
        )
        row_formats = {
            "PROJECT": {"align": '^', "width": 0.076},
            "SESSION ID": {"align": '^', "width": 0.135},
            "LOG ID": {"align": '^', "width": 0.101},
            "START": {"align": '^', "width": 0.152},
            "END": {"align": '^', "width": 0.161},
            "DURATION": {"align": '^', "width": 0.152},
            "%REPORT": {"align": '^', "width": 0.118},
            "NOTES": {"align": '<'}
        }
        return {'report_max_width': report_max_width, 'footer_fields': footer_fields,
                'row_headers': row_headers, 'row_formats': row_formats}

    def fetch_template(self):
        if self.level == 0:
            return self._project_level_template()
        elif self.level == 1:
            return self._session_level_template()
        elif self.level == 2:
            return self._log_level_template()


"""
def create_main_queue(data, summary):
    queue = ReportQueue(size=len(data))
    for row in data:
        queue.enqueue(row)


def create_report_summary():
    return ReportSummary()


def log_level_report(self):
    summary = create_report_summary()
    main_queue = create_main_queue(data, summary)


def convert_to_datetime(time):
    format = "%Y-%m-%d %H:%M:%S"
    return datetime.strptime(time, format)




def report_router(self, level, chron=False):
    if level == 0:
        pass
    if level == 1:
        pass
    if level == 2:
        pass
"""