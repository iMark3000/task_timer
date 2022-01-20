import pytest
from datetime import datetime
from datetime import timedelta

from src.timer_reports.report_printer.row_component_printer import RowPrinter
from src.timer_reports.report_constructor.report_componenets import Row
from src.timer_reports.report_constructor.report_tree.report_nodes import RootNode
from src.timer_reports.report_constructor.report_tree.report_nodes import SessionNode
from src.timer_reports.report_constructor.report_tree.report_nodes import ProjectNode
from src.timer_reports.layout.report_configuration import ROW_FIELD_LAYOUTS
from src.timer_reports.report_constructor.report_tree.report_nodes import LogNode


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
def log_node(row_data):
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

    return log


@pytest.fixture
def row_obj(log_node):
    row_list = list()
    fields = ROW_FIELD_LAYOUTS[1]
    for x in range(5):
        row = Row(log_node, fields)
        row.compile_data()
        row_list.append(row)
    return row_list


def test_rowprinter(row_obj):

    fields = ROW_FIELD_LAYOUTS[1]
    rowprinter = RowPrinter(120, fields)

    rowprinter.configure_row()
    print('\n')
    rowprinter.column_head_printer.print_headers()
    for row in row_obj:
        rowprinter.generate_row(row)

    rowprinter2 = RowPrinter(200, fields)

    rowprinter2.configure_row()
    print('\n')
    rowprinter2.column_head_printer.print_headers()
    for row in row_obj:
        rowprinter2.generate_row(row)
