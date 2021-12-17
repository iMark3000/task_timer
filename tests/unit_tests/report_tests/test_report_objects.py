from datetime import timedelta
from datetime import datetime

import pytest

from pprint import pprint

from timer_reports.report_tree.report_nodes import RootNode
from timer_reports.report_tree.report_nodes import ProjectNode
from timer_reports.report_tree.report_nodes import SessionNode
from timer_reports.report_tree.report_nodes import LogNode
from timer_reports.layout.report_componenets import Row
from timer_reports.layout.report_componenets import Section
from timer_reports.layout.report_componenets import ReportHeaderSummary
from timer_reports.layout.report_configuration import ROW_FIELD_LAYOUTS
from timer_reports.layout.report_configuration import SECTION_FOOTER_FIELD_LAYOUTS
from timer_reports.layout.report_configuration import REPORT_FOOTER_FIELD_LAYOUTS
from timer_reports.layout.report_configuration import FIELD_MAPPING
from timer_reports.layout.report_componenets import average_helper
from timer_reports.layout.report_componenets import count_helper
from timer_reports.layout.report_componenets import percent_helper


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
        'duration': timedelta(hours=1)
    }


@pytest.fixture
def node_setup(node_data):
    root = RootNode(reporting_on='Nothing', reporting_period='From 1 to 2')
    root.duration = timedelta(hours=5)

    proj = ProjectNode(node_data['project_name'], node_data['project_id'])
    proj.duration = timedelta(hours=4)
    root.add_child(proj)

    session = SessionNode(node_data['session_id'])
    session.duration = timedelta(hours=2)
    proj.add_child(session)

    log = LogNode(**node_data)
    session.add_child(log)

    return {'root': root, 'proj': proj, 'session': session, 'log': log}


def test_row_log_level(node_setup):

    node = node_setup['log']
    fields = ROW_FIELD_LAYOUTS[1]
    print(f'\n{fields}')
    row = Row(node, fields)
    row.compile_data()
    assert len(row.data) == 8
    print('\n---------------')
    pprint(row.data)


def test_row_session_level(node_setup):
    node = node_setup['session']
    fields = ROW_FIELD_LAYOUTS[2]
    row = Row(node, fields)
    row.compile_data()
    assert len(row.data) == 5
    print('\n---------------')
    pprint(row.data)


def test_section_session_level(node_setup):
    node = node_setup['session']
    fields = SECTION_FOOTER_FIELD_LAYOUTS[1]
    section = Section(node, fields, sub_section=True)
    section.compile_data()
    assert section.is_sub_section() is True
    print('\n---------------')
    pprint(section.data)


def test_section_project_level(node_setup):
    node = node_setup['proj']
    fields = SECTION_FOOTER_FIELD_LAYOUTS[1]
    section = Section(node, fields)
    section.compile_data()
    assert section.is_sub_section() is False
    # assert len(section.section_data) == 4
    print('\n---------------')
    pprint(section.data)


def test_report_head_foot_log_level(node_setup):
    node = node_setup['root']
    fields = REPORT_FOOTER_FIELD_LAYOUTS[1]
    report_header_sum = ReportHeaderSummary(node, fields)
    report_header_sum.compile_report_header()
    report_header_sum.compile_data()
    assert len(report_header_sum.header) == 2
    assert len(report_header_sum.data) == 7


def test_report_head_foot_session_level(node_setup):
    node = node_setup['root']
    fields = REPORT_FOOTER_FIELD_LAYOUTS[2]
    report_header_sum = ReportHeaderSummary(node, fields)
    report_header_sum.compile_report_header()
    report_header_sum.compile_data()
    assert len(report_header_sum.header) == 2
    assert len(report_header_sum.data) == 5


def test_report_head_foot_project_level(node_setup):
    node = node_setup['root']
    fields = REPORT_FOOTER_FIELD_LAYOUTS[3]
    report_header_sum = ReportHeaderSummary(node, fields)
    report_header_sum.compile_report_header()
    report_header_sum.compile_data()
    assert len(report_header_sum.header) == 2
    assert len(report_header_sum.data) == 7


def test_percent_helper_up_one_level(node_setup):
    node = node_setup['log']
    whole_node_type = 'SessionNode'
    percent = percent_helper(node, whole_node_type)
    assert percent == .5


def test_percent_helper_up_two_levels(node_setup):
    node = node_setup['log']
    whole_node_type = 'ProjectNode'
    percent = percent_helper(node, whole_node_type)
    assert percent == .25


def test_percent_helper_up_three_levels(node_setup):
    node = node_setup['log']
    whole_node_type = 'RootNode'
    percent = percent_helper(node, whole_node_type)
    assert percent == .2


@pytest.fixture
def count_data(node_data):
    root = RootNode(reporting_on='Nothing', reporting_period='From 1 to 2')
    root.add_child(ProjectNode('proj1', 1))
    root.add_child(ProjectNode('proj2', 2))

    proj = ProjectNode(node_data['project_name'], node_data['project_id'])
    root.add_child(proj)
    proj.add_child(SessionNode(2))
    proj.add_child(SessionNode(3))

    session = SessionNode(node_data['session_id'])
    proj.add_child(session)

    session.add_child(LogNode(**node_data))
    session.add_child(LogNode(**node_data))

    # 3 projects, 4 sessions, 4 logs
    return {'root': root, 'proj': proj, 'session': session}


def test_count_help_root_log(count_data):
    node = count_data['root']
    count_node_type = 'LogNode'
    result = count_helper(node, count_node_type)
    assert result == 2


def test_count_help_root_session(count_data):
    node = count_data['root']
    count_node_type = 'SessionNode'
    result = count_helper(node, count_node_type)
    assert result == 3


def test_count_help_root_project(count_data):
    node = count_data['root']
    count_node_type = 'ProjectNode'
    result = count_helper(node, count_node_type)
    assert result == 3


def test_count_help_project_log(count_data):
    node = count_data['proj']
    count_node_type = 'LogNode'
    result = count_helper(node, count_node_type)
    assert result == 2


def test_count_help_project_session(count_data):
    node = count_data['proj']
    count_node_type = 'SessionNode'
    result = count_helper(node, count_node_type)
    assert result == 3


def test_count_help_session_log(count_data):
    node = count_data['session']
    count_node_type = 'LogNode'
    result = count_helper(node, count_node_type)
    assert result == 2


def test_average_help_session(node_setup):
    pass


def test_average_help_project(node_setup):
    pass


def test_average_help_root(node_setup):
    pass
