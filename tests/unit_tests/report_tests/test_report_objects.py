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
from timer_reports.layout.report_configuration import SECTION_FIELD_LAYOUTS
from timer_reports.layout.report_configuration import REPORT_HEADER_FOOTER_FIELD_LAYOUTS
from timer_reports.layout.report_componenets import count_and_average_helper
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
    fields = SECTION_FIELD_LAYOUTS[1]
    section = Section(node, fields, sub_section=True)
    section.compile_data()
    assert section.is_sub_section() is not None
    print('\n---------------')
    pprint(section.data)


def test_section_project_level(node_setup):
    node = node_setup['proj']
    fields = SECTION_FIELD_LAYOUTS[1]
    section = Section(node, fields)
    section.compile_data()
    assert section.is_sub_section() is None
    # assert len(section.section_data) == 4
    print('\n---------------')
    pprint(section.data)


def test_report_head_foot_log_level(node_setup):
    node = node_setup['root']
    fields = REPORT_HEADER_FOOTER_FIELD_LAYOUTS[1]
    report_header_sum = ReportHeaderSummary(node, fields)
    report_header_sum.compile_report_header()
    report_header_sum.compile_data()
    assert len(report_header_sum.header) == 2
    assert len(report_header_sum.data) == 7


def test_report_head_foot_session_level(node_setup):
    node = node_setup['root']
    fields = REPORT_HEADER_FOOTER_FIELD_LAYOUTS[2]
    report_header_sum = ReportHeaderSummary(node, fields)
    report_header_sum.compile_report_header()
    report_header_sum.compile_data()
    assert len(report_header_sum.header) == 2
    assert len(report_header_sum.data) == 5


def test_report_head_foot_project_level(node_setup):
    node = node_setup['root']
    fields = REPORT_HEADER_FOOTER_FIELD_LAYOUTS[3]
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
    root.duration = timedelta(minutes=30)
    proj1 = ProjectNode('proj1', 1)
    proj1.duration = timedelta(minutes=5)
    proj2 = ProjectNode('proj2', 2)
    proj2.duration = timedelta(minutes=5)
    root.add_child(proj1)
    root.add_child(proj2)

    proj = ProjectNode(node_data['project_name'], node_data['project_id'])
    proj.duration = timedelta(minutes=20)
    root.add_child(proj)
    s1 = SessionNode(2)
    s1.duration = timedelta(minutes=5)
    s2 = SessionNode(3)
    s2.duration = timedelta(minutes=5)
    proj.add_child(s1)
    proj.add_child(s2)

    session = SessionNode(node_data['session_id'])
    session.duration = timedelta(minutes=10)
    proj.add_child(session)

    node1 = LogNode(**node_data)
    node1._duration = timedelta(minutes=5)
    node2 = LogNode(**node_data)
    node2._duration = timedelta(minutes=5)

    session.add_child(node1)
    session.add_child(node1)

    return {'root': root, 'proj': proj, 'session': session}


def test_count_help_root_log(count_data):
    node = count_data['root']
    count_node_type = 'LogNode'
    result = count_and_average_helper(node, count_node_type)
    assert result[0] == 2
    assert result[1] == timedelta(minutes=10)


def test_count_help_root_session(count_data):
    node = count_data['root']
    count_node_type = 'SessionNode'
    result = count_and_average_helper(node, count_node_type)
    assert result[0] == 3
    assert result[1] == timedelta(minutes=20)


def test_count_help_root_project(count_data):
    node = count_data['root']
    count_node_type = 'ProjectNode'
    result = count_and_average_helper(node, count_node_type)
    assert result[0] == 3
    assert result[1] == timedelta(minutes=30)


def test_count_help_project_log(count_data):
    node = count_data['proj']
    count_node_type = 'LogNode'
    result = count_and_average_helper(node, count_node_type)
    assert result[0] == 2
    assert result[1] == timedelta(minutes=10)


def test_count_help_project_session(count_data):
    node = count_data['proj']
    count_node_type = 'SessionNode'
    result = count_and_average_helper(node, count_node_type)
    assert result[0] == 3
    assert result[1] == timedelta(minutes=20)


def test_count_help_session_log(count_data):
    node = count_data['session']
    count_node_type = 'LogNode'
    result = count_and_average_helper(node, count_node_type)
    assert result[0] == 2
    assert result[1] == timedelta(minutes=10)


def test_average_help_session(node_setup):
    pass


def test_average_help_project(node_setup):
    pass


def test_average_help_root(node_setup):
    pass
