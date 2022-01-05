from datetime import datetime
from datetime import timedelta

import pytest
from pprint import pprint

from timer_reports.layout.report_configuration import ROW_FIELD_LAYOUTS
from timer_reports.layout.report_configuration import SECTION_FIELD_LAYOUTS
from timer_reports.layout.report_configuration import REPORT_HEADER_FOOTER_FIELD_LAYOUTS

from timer_reports.report_constructor.report_constructor import ReportPrep
from timer_reports.report_constructor.report_constructor import ReportTreeCreator
from timer_reports.report_constructor.report_constructor import ReportConstructor
from timer_reports.report_constructor.report_tree.report_nodes import ProjectNode
from timer_reports.report_constructor.report_tree.report_nodes import SessionNode
from timer_reports.report_constructor.report_tree.report_nodes import LogNode

from timer_reports.report_constructor.report_componenets import Row
from timer_reports.report_constructor.report_componenets import Section
from timer_reports.report_constructor.report_componenets import ReportHeaderSummary


from timer_reports.report_printer.row_printer import RowPrinter
from timer_reports.report_printer.section_printer import SectionPrinter
from timer_reports.report_printer.report_head_foot_printer import ReportHeadFootPrinter


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
    dates = ('11/15/2021', '11/22/2021')
    p_ids = ('4', '3')
    return ReportPrep(dates, p_ids, query_data)


def test_report_tree_creator(create_report_prep_for_test):
    report = create_report_prep_for_test
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


@pytest.fixture()
def create_tree(create_report_prep_for_test):
    report = create_report_prep_for_test
    report.prep_report()
    report_data = report.export_data_for_tree()
    tree_constructor = ReportTreeCreator(**report_data)
    tree_constructor.build_tree()
    return tree_constructor.get_tree()


def test_report_constructor(create_tree):
    report_constructor = ReportConstructor(create_tree, 1, LogNode, [ProjectNode, SessionNode])
    report_constructor.construct()
    result = report_constructor.get_report_components()
    print('\n')
    for r in result:
        print(r)
    assert len(result) == 16


@pytest.fixture
def create_report_components(create_tree):
    report_constructor = ReportConstructor(create_tree, 1, LogNode, [ProjectNode, SessionNode])
    report_constructor.construct()
    return report_constructor.get_report_components()


def test_printers(create_report_components):
    print('\n')
    header_footer = ReportHeadFootPrinter(150, REPORT_HEADER_FOOTER_FIELD_LAYOUTS[1])
    header_footer.configure()
    section = SectionPrinter(150, SECTION_FIELD_LAYOUTS[1])
    section.configure()
    row = RowPrinter(150, ROW_FIELD_LAYOUTS[1])
    row.configure_row()
    row.set_column_head_printer()

    current_section = None
    head_component = None

    for component in create_report_components:
        if isinstance(component, ReportHeaderSummary):
            header_footer.print_report_header(component)
            head_component = component
        elif isinstance(component, Section):
            section.print_section_header(component)
            if not component.is_sub_section(): # Where are sections being made primary and sub?
                if current_section is None:
                    current_section = component
                else:
                    section.print_section_foot(current_section)
                    current_section = component
            else:
                row.column_head_printer.print_headers()
        elif isinstance(component, Row):
            row.generate_row(component)
    section.print_section_foot(current_section)
    header_footer.print_report_summary(head_component)

