from typing import List, Tuple
from datetime import datetime



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