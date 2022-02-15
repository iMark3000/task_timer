from datetime import timedelta
from datetime import datetime
import pytest

from pprint import pprint

from src.timer_reports.report_constructor.report_tree.report_nodes import RootNode
from src.timer_reports.report_constructor.report_tree.report_nodes import ProjectNode
from src.timer_reports.report_constructor.report_tree.report_nodes import SessionNode
from src.timer_reports.report_constructor.report_tree.report_nodes import LogNode
from src.timer_reports.report_constructor.report_componenets import Row
from src.timer_reports.report_constructor.report_componenets import Section
from src.timer_reports.report_constructor.report_componenets import ReportHeaderSummary
from src.timer_reports.layout.report_configuration import ROW_FIELD_LAYOUTS
from src.timer_reports.layout.report_configuration import SECTION_FIELD_LAYOUTS
from src.timer_reports.layout.report_configuration import REPORT_HEADER_FOOTER_FIELD_LAYOUTS
from src.timer_reports.report_constructor.report_componenets import count_helper
from src.timer_reports.report_constructor.report_constructor import total_duration_helper
from src.timer_reports.report_constructor.report_componenets import percent_helper
from src.timer_reports.report_constructor.report_constructor import ReportPrep
from src.timer_reports.report_constructor.report_constructor import ReportTreeCreator


@pytest.fixture
def node_data():
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
def create_report_prep_for_test(node_data):
    dates = ('11/15/2021', '11/22/2021')
    p_ids = ('4', '3')
    return ReportPrep(dates, p_ids, node_data)


@pytest.fixture()
def create_tree(create_report_prep_for_test):
    report = create_report_prep_for_test
    report.prep_report()
    report_data = report.export_data_for_tree()
    tree_constructor = ReportTreeCreator(**report_data)
    tree_constructor.build_tree()
    return tree_constructor.get_tree()

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
    assert len(report_header_sum.data) == 9


def test_report_head_foot_session_level(node_setup):
    node = node_setup['root']
    fields = REPORT_HEADER_FOOTER_FIELD_LAYOUTS[2]
    report_header_sum = ReportHeaderSummary(node, fields)
    report_header_sum.compile_report_header()
    report_header_sum.compile_data()
    assert len(report_header_sum.data) == 7


def test_report_head_foot_project_level(node_setup):
    node = node_setup['root']
    fields = REPORT_HEADER_FOOTER_FIELD_LAYOUTS[3]
    report_header_sum = ReportHeaderSummary(node, fields)
    report_header_sum.compile_report_header()
    report_header_sum.compile_data()
    assert len(report_header_sum.data) == 9


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
    proj1 = ProjectNode('proj1', 1)
    proj2 = ProjectNode('proj2', 2)
    root.add_child(proj1)
    root.add_child(proj2)

    proj = ProjectNode(node_data['project_name'], node_data['project_id'])
    root.add_child(proj)
    s1 = SessionNode(2)
    s2 = SessionNode(3)
    proj.add_child(s1)
    proj.add_child(s2)

    session = SessionNode(node_data['session_id'])
    proj.add_child(session)

    node1 = LogNode(**node_data)
    node1._duration = timedelta(minutes=5)
    node2 = LogNode(**node_data)
    node2._duration = timedelta(minutes=5)

    session.add_child(node1)
    session.add_child(node2)

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


def test_total_duration_root(node_setup):
    result = total_duration_helper()


def test_total_duration_project(node_setup):
    pass


def test_total_duration_session(node_setup):
    pass
