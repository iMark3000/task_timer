from datetime import timedelta

import pytest
from pprint import pprint

from timer_reports.report_tree.report_tree import ReportTree
from timer_reports.report import ReportPrep
from timer_reports.report import ReportTreeCreator
from timer_reports.report_tree.report_nodes import ProjectNode
from timer_reports.report_tree.report_nodes import SessionNode
from timer_reports.report_tree.report_nodes import LogNode


@pytest.fixture
def query_data():
    return [
        {'project_name': 'cat',
         'project_id': 3,
         'session_id': 3,
         'session_note': None,
         'log_id': 5,
         'start_time': '2021-11-17 11:07:11',
         'end_time': '2021-11-17 11:07:37.923870',
         'start_log_note': None,
         'end_log_note': None},
        {'project_name': 'cat',
         'project_id': 3,
         'session_id': 4,
         'session_note': None,
         'log_id': 6,
         'start_time': '2021-11-17 11:26:58',
         'end_time': '2021-11-17 11:27:10.419275',
         'start_log_note': 'Testing this out',
         'end_log_note': 'How do you handle this?'},
        {'project_name': 'cat',
         'project_id': 3,
         'session_id': 5,
         'session_note': None,
         'log_id': 7,
         'start_time': '2021-11-17 11:20:00',
         'end_time': '2021-11-17 11:34:00',
         'start_log_note': None,
         'end_log_note': None},
        {'project_name': 'cat',
         'project_id': 3,
         'session_id': 5,
         'session_note': None,
         'log_id': 8,
         'start_time': '2021-11-17 11:40:00',
         'end_time': '2021-11-17 11:55:42.765024',
         'start_log_note': None,
         'end_log_note': None},
        {'project_name': 'cat',
         'project_id': 3,
         'session_id': 6,
         'session_note': None,
         'log_id': 9,
         'start_time': '2021-11-17 11:20:00',
         'end_time': '2021-11-17 11:34:00',
         'start_log_note': None,
         'end_log_note': None},
        {'project_name': 'cat',
         'project_id': 3,
         'session_id': 6,
         'session_note': None,
         'log_id': 10,
         'start_time': '2021-11-17 11:40:00',
         'end_time': '2021-11-17 12:08:42.438854',
         'start_log_note': None,
         'end_log_note': None},
        {'project_name': 'cadabada',
         'project_id': 4,
         'session_id': 8,
         'session_note': None,
         'log_id': 12,
         'start_time': '2021-11-17 10:23:00',
         'end_time': '2021-11-17 11:05:00',
         'start_log_note': None,
         'end_log_note': None},
        {'project_name': 'cadabada',
         'project_id': 4,
         'session_id': 8,
         'session_note': None,
         'log_id': 13,
         'start_time': '2021-11-17 11:05:00',
         'end_time': '2021-11-17 12:11:02.103525',
         'start_log_note': None,
         'end_log_note': None}]


@pytest.fixture
def create_report_constructor(query_data):
    dates = ('11/15/2021', '11/22/2021')
    p_ids = ('4', '3')
    return ReportPrep(1, dates, p_ids, query_data)


def test_report_constructor(create_report_constructor):
    report = create_report_constructor
    report.prep_report()
    report_data = report.export_data_for_tree()
    assert len(report_data) == 3
    assert len(report_data["report_data_for_tree"]) == 8
    pprint(report_data)


def test_report_tree_creator(create_report_constructor):
    report = create_report_constructor
    report.prep_report()
    report_data = report.export_data_for_tree()
    tree_constructor = ReportTreeCreator(**report_data)
    tree_constructor.build_tree()
    tree = tree_constructor.get_tree()
    assert tree.root.reporting_on == 'cat & cadabada'
    assert tree.root.reporting_period == '11/15/2021 to 11/22/2021'
    assert len(tree.root.children) == 2
    assert tree.root.duration == timedelta(seconds=10864)
    # checking structure
    for child in tree.root.children:
        assert isinstance(child, ProjectNode)
        for c in child.children:
            assert isinstance(c, SessionNode)
            for leaf in c.children:
                assert isinstance(leaf, LogNode)
