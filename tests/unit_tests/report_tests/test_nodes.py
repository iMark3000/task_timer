from datetime import timedelta
from datetime import datetime

import pytest

from timer_reports.report_tree.report_tree import ReportTree
from timer_reports.report_tree.report_nodes import RootNode
from timer_reports.report_tree.report_nodes import ProjectNode
from timer_reports.report_tree.report_nodes import SessionNode
from timer_reports.report_tree.report_nodes import LogNode


@pytest.fixture
def node_data():
    return {
        'end_log_note': 'Test note...again',
        'end_time': datetime(year=2021, month=11, day=17, hour=11, minute=7, second=37),
        'session_note': None,
        'session_id': 3,
        'log_id': 5,
        'start_log_note': 'Test note',
        'start_time': datetime(year=2021, month=11, day=17, hour=11, minute=7, second=11),
        'project_name': 'cat',
        'project_id': 3,
        'duration': timedelta(hours=3, minutes=10)
    }


@pytest.fixture
def project_node(node_data):
    return ProjectNode(node_data['project_name'], node_data['project_id'])


@pytest.fixture
def session_node(node_data):
    return SessionNode(node_data['session_id'])


def test_project_node(node_data):
    node = ProjectNode(node_data['project_name'], node_data['project_id'])
    node.duration = node_data['duration']
    assert node.project_id == 3
    assert node.project_name == 'cat'
    assert node.duration == timedelta(hours=3, minutes=10)
    assert len(node.children) == 0
    node.duration = timedelta(hours=3, minutes=10)
    assert node.duration == timedelta(hours=6, minutes=20)
    print(f'\n{node}')


def test_session_node(node_data):
    node = SessionNode(node_data['session_id'])
    node.duration = node_data['duration']
    assert node.session_id == 3
    assert node.duration == timedelta(hours=3, minutes=10)
    assert len(node.children) == 0
    node.duration = timedelta(hours=3, minutes=10)
    assert node.duration == timedelta(hours=6, minutes=20)
    print(f'\n{node}')


def test_log_node(node_data):
    node = LogNode(**node_data)
    assert node.project_id == 3
    assert node.project_name == 'cat'
    assert node.session_id == 3
    assert node.log_id == 5
    assert node.start_time == datetime(year=2021, month=11, day=17, hour=11, minute=7, second=11)
    assert node.end_time == datetime(year=2021, month=11, day=17, hour=11, minute=7, second=37)
    assert node.start_log_note == 'Test note'
    assert node.end_log_note == 'Test note...again'
    assert node.duration == timedelta(hours=3, minutes=10)
    print(f'\n{node}')


def test_session_project_relationship(node_data, project_node):
    node = SessionNode(node_data['session_id'])
    project_node.add_child(node)
    assert node.parent == project_node
    assert len(project_node.children) == 1
    assert project_node.children[0] == node


def test_log_session_relationship(node_data, session_node):
    node = LogNode(**node_data)
    session_node.add_child(node)
    assert node.parent == session_node
    assert len(session_node.children) == 1
    assert session_node.children[0] == node
