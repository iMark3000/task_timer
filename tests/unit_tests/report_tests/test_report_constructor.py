from datetime import datetime
from datetime import timedelta

import pytest
from pprint import pprint

from src.timer_reports.layout.layout_manager import LayoutManager

from src.timer_reports.report_constructor.report_constructor import ReportPrep
from src.timer_reports.report_constructor.report_constructor import ReportTreeCreator
from src.timer_reports.report_constructor.report_constructor import ReportConstructor
from src.timer_reports.report_constructor.report_constructor import total_duration_helper

from src.timer_reports.report_constructor.report_tree.report_nodes import ProjectNode
from src.timer_reports.report_constructor.report_tree.report_nodes import SessionNode
from src.timer_reports.report_constructor.report_tree.report_nodes import LogNode

from src.timer_reports.report import create_report

from src.timer_reports.report_printer.printer_manager import ReportPrinter


@pytest.fixture
def query_data():
    return [
        {'project_name': 'fish',
         'project_id': 1,
         'session_id': 1,
         'session_note': None,
         'log_id': 1,
         'start_timestamp': '2021-11-17 11:00:00.0',
         'end_timestamp': '2021-11-17 12:00:00.0',
         'start_log_note': None,
         'end_log_note': None},
        {'project_name': 'cat',
         'project_id': 2,
         'session_id': 2,
         'session_note': None,
         'log_id': 2,
         'start_timestamp': '2021-11-18 11:00:00.0',
         'end_timestamp': '2021-11-18 11:30:00.0',
         'start_log_note': None,
         'end_log_note': None},
        {'project_name': 'cat',
         'project_id': 2,
         'session_id': 3,
         'session_note': None,
         'log_id': 3,
         'start_timestamp': '2021-11-18 13:00:00.0',
         'end_timestamp': '2021-11-18 14:00:00.0',
         'start_log_note': None,
         'end_log_note': None},
        {'project_name': 'bird',
         'project_id': 3,
         'session_id': 4,
         'session_note': None,
         'log_id': 4,
         'start_timestamp': '2021-11-21 13:15:00.0',
         'end_timestamp': '2021-11-21 13:30:00.0',
         'start_log_note': None,
         'end_log_note': None},
        {'project_name': 'bird',
         'project_id': 3,
         'session_id': 4,
         'session_note': None,
         'log_id': 5,
         'start_timestamp': '2021-11-21 15:00:00.0',
         'end_timestamp': '2021-11-21 17:00:00.0',
         'start_log_note': None,
         'end_log_note': None},
        {'project_name': 'bird',
         'project_id': 3,
         'session_id': 5,
         'session_note': None,
         'log_id': 6,
         'start_timestamp': '2021-11-22 9:00:00.0',
         'end_timestamp': '2021-11-22 10:00:00.0',
         'start_log_note': None,
         'end_log_note': None},
        {'project_name': 'bird',
         'project_id': 3,
         'session_id': 5,
         'session_note': None,
         'log_id': 7,
         'start_timestamp': '2021-11-22 12:00:00.0',
         'end_timestamp': '2021-11-22 13:30:00.0',
         'start_log_note': None,
         'end_log_note': None},
        {'project_name': 'bird',
         'project_id': 3,
         'session_id': 6,
         'session_note': None,
         'log_id': 8,
         'start_timestamp': '2021-11-23 12:00:00.0',
         'end_timestamp': '2021-11-23 12:30:00.0',
         'start_log_note': None,
         'end_log_note': None},
        {'project_name': 'bird',
         'project_id': 3,
         'session_id': 6,
         'session_note': None,
         'log_id': 9,
         'start_timestamp': '2021-11-24 11:00:00.0',
         'end_timestamp': '2021-11-24 13:30:00.0',
         'start_log_note': None,
         'end_log_note': None},
        {'project_name': 'dolphin',
         'project_id': 4,
         'session_id': 7,
         'session_note': None,
         'log_id': 10,
         'start_timestamp': '2021-11-27 11:00:00.0',
         'end_timestamp': '2021-11-27 11:15:00.0',
         'start_log_note': None,
         'end_log_note': None},
        {'project_name': 'dolphin',
         'project_id': 4,
         'session_id': 7,
         'session_note': None,
         'log_id': 11,
         'start_timestamp': '2021-11-28 11:00:00.0',
         'end_timestamp': '2021-11-28 12:15:00.0',
         'start_log_note': None,
         'end_log_note': None},
        {'project_name': 'dolphin',
         'project_id': 4,
         'session_id': 7,
         'session_note': None,
         'log_id': 12,
         'start_timestamp': '2021-11-30 11:00:00.0',
         'end_timestamp': '2021-11-30 11:30:00.0',
         'start_log_note': None,
         'end_log_note': None},
        {'project_name': 'dolphin',
         'project_id': 4,
         'session_id': 8,
         'session_note': None,
         'log_id': 13,
         'start_timestamp': '2021-11-30 13:00:00.0',
         'end_timestamp': '2021-11-30 14:00:00.0',
         'start_log_note': None,
         'end_log_note': None}
        ]


def test_report_prep(query_data):
    dates = ('11/15/2021', '11/22/2021')
    p_ids = ('4', '3')
    report = ReportPrep(dates, p_ids, query_data)
    report.prep_report()
    result = report.export_data_for_tree()
    sample_keys = result["report_data_for_tree"][0].keys()
    sample_log = result["report_data_for_tree"][0]
    assert len(result) == 3
    assert result["reporting_on"] == 'cat & cadabada'
    assert result["reporting_period"] == '11/15/2021 to 11/22/2021'
    assert len(result["report_data_for_tree"]) == 8
    assert 'duration' in sample_keys
    assert isinstance(sample_log["start_time"], datetime)
    assert isinstance(sample_log["duration"], timedelta)


@pytest.fixture
def create_report_prep_for_test(query_data):
    dates = (datetime(year=2021, month=11, day=15), datetime(year=2021, month=11, day=30))
    return ReportPrep(dates, query_data)


def test_report_tree_creator(create_report_prep_for_test):
    report = create_report_prep_for_test
    report.prep_report()
    report_data = report.export_data_for_tree()
    tree_constructor = ReportTreeCreator(**report_data)
    tree_constructor.build_tree()
    tree = tree_constructor.get_tree()
    assert tree.root.reporting_on == 'MULTIPLE PROJECTS'
    assert tree.root.reporting_period == '11/15/2021 to 11/30/2021'
    assert len(tree.root.children) == 4
    # checking structure
    for child in tree.root.children:
        assert isinstance(child, ProjectNode)
        for c in child.children:
            assert isinstance(c, SessionNode)
            for leaf in c.children:
                assert isinstance(leaf, LogNode)


@pytest.fixture()
def create_tree(create_report_prep_for_test):
    report = create_report_prep_for_test
    report.prep_report()
    report_data = report.export_data_for_tree()
    tree_constructor = ReportTreeCreator(**report_data)
    tree_constructor.build_tree()
    return tree_constructor.get_tree()


def test_duration_calculation(create_tree):
    total_duration_helper(create_tree)
    for project in create_tree.root.children:
        print(f'\n{project} -- {project.duration}')
        for session in project.children:
            print(f'{session} -- {session.duration}')
            for log in session.children:
                print(f'{log} -- {log.duration}')


def test_create_layout_manager_config_1():
    manager = LayoutManager(1)
    manager.set_up_layout()
    assert manager.report_width == 118
    assert manager.report_row == LogNode
    assert len(manager.report_sections) == 2
    assert len(manager.report_header_footer_fields) == 2
    assert len(manager.report_section_fields) == 2
    assert len(manager.report_row_fields) == 1


def test_create_layout_manager_config_2():
    manager = LayoutManager(2)
    manager.set_up_layout()
    assert manager.report_width == 118
    assert manager.report_row == SessionNode
    assert len(manager.report_sections) == 1
    assert len(manager.report_header_footer_fields) == 2
    assert len(manager.report_section_fields) == 2
    assert len(manager.report_row_fields) == 1


@pytest.fixture
def create_layout_manager_config1():
    manager = LayoutManager(1)
    manager.set_up_layout()
    return manager


@pytest.fixture
def create_layout_manager_config2():
    manager = LayoutManager(2)
    manager.set_up_layout()
    return manager


def test_report_constructor(create_tree, create_layout_manager_config1):
    total_duration_helper(create_tree)
    report_constructor = ReportConstructor(create_tree, create_layout_manager_config1)
    report_constructor.construct()
    result = report_constructor.get_report_components()
    print('\n')
    for r in result:
        r.compile_data()
        print('\n---------------')
        print(r)
        pprint(r.data)
    assert len(result) == 16


@pytest.fixture
def create_report_components(create_tree, create_layout_manager_config1):
    total_duration_helper(create_tree)
    report_constructor = ReportConstructor(create_tree, create_layout_manager_config1)
    report_constructor.construct()
    return report_constructor.get_report_components()


def test_printers(create_report_components, create_layout_manager_config1):
    report_printer = ReportPrinter(create_layout_manager_config1)
    report_printer.set_up_component_printers()
    print('\n')
    for component in create_report_components:
        component.compile_data()
        print(f'{component.data}')

    print('\n')
    for component in create_report_components:
        component.compile_data()
        report_printer.print_component(component)
    report_printer.end_report_printing_process()


def test_create_report_func(query_data):
    data = dict()
    dates = ('11/15/2021', '11/22/2021')
    p_ids = ('4', '3')
    data["reporting_period"] = dates
    data["reporting_on"] = p_ids
    data["reporting_level"] = 2
    data["report_query"] = query_data

    create_report(data)
