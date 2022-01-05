from datetime import datetime
from datetime import timedelta

import pytest

from timer_reports.report_constructor.report_tree.report_tree import ReportTree
from timer_reports.report_constructor.report_tree.report_nodes import RootNode
from timer_reports.report_constructor.report_tree.report_nodes import LogNode


@pytest.fixture
def query_data():
    return [
        {'end_log_note': None,
         'end_time': datetime(year=2021, month=11, day=17, hour=11, minute=7, second=37),
         'session_note': None,
         'session_id': 3,
         'start_log_note': None,
         'start_time': datetime(year=2021, month=11, day=17, hour=11, minute=7, second=37),
         'project_name': 'cat',
         'project_id': 3,
         'log_id': 23,
         'duration': timedelta(hours=3)},
        {'end_log_note': None,
         'end_time': datetime(year=2021, month=11, day=17, hour=11, minute=7, second=37),
         'session_note': None,
         'session_id': 4,
         'start_log_note': None,
         'start_time': datetime(year=2021, month=11, day=17, hour=11, minute=7, second=37),
         'project_name': 'cat',
         'project_id': 3,
         'log_id': 32,
         'duration': timedelta(hours=3)},
        {'end_log_note': None,
         'end_time': datetime(year=2021, month=11, day=17, hour=11, minute=7, second=37),
         'session_note': None,
         'session_id': 5,
         'start_log_note': None,
         'start_time': datetime(year=2021, month=11, day=17, hour=11, minute=7, second=37),
         'project_name': 'cat',
         'project_id': 3,
         'log_id': 79,
         'duration': timedelta(hours=3)},
        {'end_log_note': None,
         'end_time': datetime(year=2021, month=11, day=17, hour=11, minute=7, second=37),
         'session_note': None,
         'session_id': 5,
         'start_log_note': None,
         'start_time': datetime(year=2021, month=11, day=17, hour=11, minute=7, second=37),
         'project_name': 'cat',
         'project_id': 3,
         'log_id': 21,
         'duration': timedelta(hours=3)},
        {'end_log_note': None,
         'end_time': datetime(year=2021, month=11, day=17, hour=11, minute=7, second=37),
         'session_note': None,
         'session_id': 6,
         'start_log_note': None,
         'start_time': datetime(year=2021, month=11, day=17, hour=11, minute=7, second=37),
         'project_name': 'cat',
         'project_id': 3,
         'log_id': 44,
         'duration': timedelta(hours=3)},
        {'end_log_note': None,
         'end_time': datetime(year=2021, month=11, day=17, hour=11, minute=7, second=37),
         'session_note': None,
         'session_id': 19,
         'start_log_note': None,
         'start_time': datetime(year=2021, month=11, day=17, hour=11, minute=7, second=37),
         'project_name': 'moose',
         'project_id': 6,
         'log_id': 75,
         'duration': timedelta(hours=3)}
    ]


def test_root():
    tree = ReportTree()
    root = RootNode('test project', '11/5 to 11/22')
    tree.root = root
    assert tree.root.reporting_on == 'test project'
    assert tree.root.reporting_period == '11/5 to 11/22'


def test_project_nodes(query_data):
    tree = ReportTree()
    root = RootNode('test project', '11/5 to 11/22')
    tree.root = root
    for d in query_data:
        node = LogNode(**d)
        tree.add_node(tree.root, node)

    assert len(tree.root.children) == 2


def test_session_nodes(query_data):
    total_sessions = 0
    tree = ReportTree()
    root = RootNode('test project', '11/5 to 11/22')
    tree.root = root
    for d in query_data:
        node = LogNode(**d)
        tree.add_node(tree.root, node)

    for child in tree.root.children:
        total_sessions += len(child.children)

    assert total_sessions == 5


def test_log_nodes(query_data):
    tree = ReportTree()
    root = RootNode('test project', '11/5 to 11/22')
    tree.root = root
    for d in query_data:
        node = LogNode(**d)
        tree.add_node(tree.root, node)

    total_logs = 0
    for child in tree.root.children:    # Root looking at projects
        for c in child.children:    # projects looking at sessions
            total_logs += len(c.children)

    assert total_logs == len(query_data)
