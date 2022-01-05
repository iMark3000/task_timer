import pytest
from datetime import datetime
from datetime import timedelta

from timer_reports.report_printer.report_head_foot_printer import ReportHeadFootPrinter
from timer_reports.report_constructor.report_componenets import ReportHeaderSummary
from timer_reports.report_constructor.report_tree.report_nodes import RootNode
from timer_reports.report_constructor.report_tree.report_nodes import ProjectNode
from timer_reports.report_constructor.report_tree.report_nodes import SessionNode
from timer_reports.report_constructor.report_tree.report_nodes import LogNode
from timer_reports.layout.report_configuration import REPORT_HEADER_FOOTER_FIELD_LAYOUTS


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


def test_report_header_footer(set_up_nodes):
    print('\n')

    fields = REPORT_HEADER_FOOTER_FIELD_LAYOUTS[1]
    node = set_up_nodes["root"]
    header_footer = ReportHeaderSummary(node, fields)

    header_footer.compile_data()
    header_footer.compile_report_header()

    printer = ReportHeadFootPrinter(120, fields)
    printer.configure()
    printer.print_report_header(header_footer)
    print('\n')
    printer.print_report_summary(header_footer)
