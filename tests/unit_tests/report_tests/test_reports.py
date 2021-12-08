import pytest

from timer_reports.report import report_prep
from command_classes.commands import QueryCommand
from utils.command_enums import InputType


@pytest.fixture
def query_data():
    return [
        {'project': 'cat', 'project_id': 3, 'session': 3, 'note': None, 'logID': 5, 'startTime': '2021-11-17 11:07:11',
         'endTime': '2021-11-17 11:07:37.923870', 'startLogNote': None, 'endLogNote': None},
        {'project': 'cat', 'project_id': 3, 'session': 4, 'note': None, 'logID': 6, 'startTime': '2021-11-17 11:26:58',
         'endTime': '2021-11-17 11:27:10.419275', 'startLogNote': 'Testing this shit out',
         'endLogNote': 'How do you handle this?'},
        {'project': 'cat', 'project_id': 3, 'session': 5, 'note': None, 'logID': 7, 'startTime': '2021-11-17 11:20:00',
         'endTime': '2021-11-17 11:34:00', 'startLogNote': None, 'endLogNote': None},
        {'project': 'cat', 'project_id': 3, 'session': 5, 'note': None, 'logID': 8, 'startTime': '2021-11-17 11:40:00',
         'endTime': '2021-11-17 11:55:42.765024', 'startLogNote': None, 'endLogNote': None},
        {'project': 'cat', 'project_id': 3, 'session': 6, 'note': None, 'logID': 9, 'startTime': '2021-11-17 11:20:00',
         'endTime': '2021-11-17 11:34:00', 'startLogNote': None, 'endLogNote': None},
        {'project': 'cat', 'project_id': 3, 'session': 6, 'note': None, 'logID': 10, 'startTime': '2021-11-17 11:40:00',
         'endTime': '2021-11-17 12:08:42.438854', 'startLogNote': None, 'endLogNote': None},
        {'project': 'cadabada', 'project_id': 4, 'session': 8, 'note': None, 'logID': 12,
         'startTime': '2021-11-17 10:23:00', 'endTime': '2021-11-17 11:05:00', 'startLogNote': None,
         'endLogNote': None},
        {'project': 'cadabada', 'project_id': 4, 'session': 8, 'note': None, 'logID': 13,
         'startTime': '2021-11-17 11:05:00', 'endTime': '2021-11-17 12:11:02.103525', 'startLogNote': None,
         'endLogNote': None}]


def test_report_prep(query_data):
    args = {'chron': True}
    command = QueryCommand(InputType.QUERY, **args)
    result = report_prep(command, query_data)
    assert len(result) == 8

