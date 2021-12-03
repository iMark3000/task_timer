from typing import List
from datetime import datetime

from command_classes.commands import QueryCommand
from report_tree import ReportQueue
from report_tree import ReportSummary
from report_tree import ReportQueuePrint


def report_prep(command: QueryCommand, data: List[dict]):
    for d in data:
        d['startTime'] = convert_to_datetime(handle_microseconds(d['startTime']))
        d['endTime'] = convert_to_datetime(handle_microseconds(d['endTime']))
        d['duration'] = d['endTime'] - d['startTime']
    if command.is_chron:
        data.sort(key=lambda x: x['startTime'])
    else:
        data.sort(key=lambda x: (x['project_id'], x['session'], x['logID']))


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


def handle_microseconds(tstamp):
    # Todo: Make better
    if '.' in tstamp:
        return tstamp.split('.')[0]
    else:
        return tstamp


def report_router(self, level, chron=False):
    if level == 0:
        pass
    if level == 1:
        pass
    if level == 2:
        pass