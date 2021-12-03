from datetime import datetime

from report_tree import ReportTree
from report_nodes import RootNode
from report_nodes import LogNode


def report_prep(data, command=False):
    for d in data:
        d['startTime'] = convert_to_datetime(handle_microseconds(d['startTime']))
        d['endTime'] = convert_to_datetime(handle_microseconds(d['endTime']))
        d['duration'] = d['endTime'] - d['startTime']
    if command is False:
        data.sort(key=lambda x: x['startTime'])
    else:
        data.sort(key=lambda x: (x['project_id'], x['session'], x['logID']))


def convert_to_datetime(time):
    format = "%Y-%m-%d %H:%M:%S"
    return datetime.strptime(time, format)


def handle_microseconds(tstamp):
    # Todo: Make better
    if '.' in tstamp:
        return tstamp.split('.')[0]
    else:
        return tstamp


def report_tree_setup(data):
    tree = ReportTree
    tree.root = RootNode()

    for d in data:
        tree.add_node(tree.root, LogNode(**d))

    return tree
