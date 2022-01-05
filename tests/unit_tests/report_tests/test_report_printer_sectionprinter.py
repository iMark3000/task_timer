import pytest
from datetime import datetime
from datetime import timedelta

from timer_reports.report_printer.section_printer import SectionPrinter
from timer_reports.report_constructor.report_componenets import Section
from timer_reports.report_constructor.report_tree.report_nodes import RootNode
from timer_reports.report_constructor.report_tree.report_nodes import ProjectNode
from timer_reports.report_constructor.report_tree.report_nodes import SessionNode
from timer_reports.report_constructor.report_tree.report_nodes import LogNode
from timer_reports.layout.report_configuration import SECTION_FIELD_LAYOUTS


@pytest.fixture
def row_data():
    return {'log_id': 22,
            'project_name': 'Name',
            'project_id': 123,
            'session_id': 22,
            'start_time': datetime(year=2021, month=12, day=12, hour=12, minute=5),
            'end_time': datetime(year=2021, month=12, day=12, hour=12, minute=12),
            'duration': timedelta(minutes=7),
            'percent_SessionNode': .75,
            'percent_ProjectNode': .57,
            'start_log_note': None,
            'end_log_note': None
    }


@pytest.fixture
def set_up_nodes(row_data):
    root = RootNode(reporting_on='Nothing', reporting_period='From 1 to 2')
    root.duration = timedelta(hours=5)
    proj = ProjectNode(row_data['project_name'], row_data['project_id'])
    proj.duration = timedelta(hours=4)
    root.add_child(proj)
    session = SessionNode(row_data['session_id'])
    session.duration = timedelta(hours=2)
    proj.add_child(session)
    log = LogNode(**row_data)
    session.add_child(log)
    return {"root": root, "proj": proj, "session": session, "log": log}


def test_sectionprinter_proj(set_up_nodes):
    print('\n')

    fields = SECTION_FIELD_LAYOUTS[1]
    node = set_up_nodes["proj"]

    section = Section(node, fields)
    section.compile_data()

    section_printer = SectionPrinter(120, fields)
    section_printer.configure()
    section_printer.print_section_header(section)
    print('\n')
    section_printer.print_section_foot(section)


def test_sectionprinter_session(set_up_nodes):
    print('\n')

    fields = SECTION_FIELD_LAYOUTS[1]

    node = set_up_nodes["session"]

    section = Section(node, fields, sub_section=True)
    section.compile_data()

    section_printer = SectionPrinter(120, fields)
    section_printer.configure()
    section_printer.print_section_header(section)
    print('\n')
    section_printer.print_section_foot(section)
