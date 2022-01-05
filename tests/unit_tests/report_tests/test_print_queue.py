import pytest
from datetime import timedelta
from datetime import datetime

# Importing Nodes
from timer_reports.report_constructor.report_tree.report_nodes import RootNode
from timer_reports.report_constructor.report_tree.report_nodes import ProjectNode
from timer_reports.report_constructor.report_tree.report_nodes import SessionNode
from timer_reports.report_constructor.report_tree.report_nodes import LogNode

# Importing Report Components
from timer_reports.report_constructor.report_componenets import ReportHeaderSummary
from timer_reports.report_constructor.report_componenets import Section
from timer_reports.report_constructor.report_componenets import Row

# Importing Report Configurations
from timer_reports.layout.report_configuration import ROW_FIELD_LAYOUTS
from timer_reports.layout.report_configuration import SECTION_FIELD_LAYOUTS
from timer_reports.layout.report_configuration import REPORT_HEADER_FOOTER_FIELD_LAYOUTS


@pytest.fixture
def log_data():
    # Data for Testing
    data = {
        "log1": {
            'end_log_note': None,
            'end_time': datetime(year=2021, month=11, day=17, hour=11, minute=7, second=37),
            'session_note': None,
            'session_id': 3,
            'log_id': 5,
            'start_log_note': None,
            'start_time': datetime(year=2021, month=11, day=17, hour=10, minute=0, second=17),
            'project_name': 'cat',
            'project_id': 3,
            'duration': timedelta(hours=1, minutes=7, seconds=30)},
        "log2": {
            'end_log_note': 'Test note...again',
            'end_time': datetime(year=2021, month=11, day=18, hour=11, minute=45, second=45),
            'session_note': None,
            'session_id': 3,
            'log_id': 4,
            'start_log_note': 'Test note',
            'start_time': datetime(year=2021, month=11, day=18, hour=8, minute=15, second=15),
            'project_name': 'cat',
            'project_id': 3,
            'duration': timedelta(hours=3, minutes=30, seconds=30)},
        "log3": {
            'end_log_note': None,
            'end_time': datetime(year=2021, month=11, day=20, hour=15, minute=30, second=35),
            'session_note': None,
            'session_id': 6,
            'log_id': 9,
            'start_log_note': None,
            'start_time': datetime(year=2021, month=11, day=20, hour=14, minute=20, second=25),
            'project_name': 'walrus',
            'project_id': 7,
            'duration': timedelta(hours=1, minutes=10, seconds=10)},
        "log4": {
            'end_log_note': None,
            'end_time': datetime(year=2021, month=11, day=21, hour=18, minute=35, second=30),
            'session_note': None,
            'session_id': 6,
            'log_id': 20,
            'start_log_note': None,
            'start_time': datetime(year=2021, month=11, day=21, hour=15, minute=5, second=15),
            'project_name': 'walrus',
            'project_id': 7,
            'duration': timedelta(hours=3, minutes=30, seconds=15)},
    }
    return data


@pytest.fixture
def nodes(log_data):
    # Generating Nodes with testing data
    root = RootNode('projects 3 & 7', '11/17/2021 to 11/21/2021')
    root.duration = timedelta(hours=9, minutes=18, seconds=35)
    proj1 = ProjectNode(log_data["log1"]["project_id"], log_data["log3"]["project_name"])
    proj1.duration = timedelta(hours=4, minutes=38)
    proj2 = ProjectNode(log_data["log3"]["project_id"], log_data["log3"]["project_name"])
    proj2.duration = timedelta(hours=4, minutes=40, seconds=35)
    root.add_child(proj1)
    root.add_child(proj2)
    session1 = SessionNode(log_data["log1"]["session_id"])
    session1.duration = timedelta(hours=4, minutes=38)
    proj1.add_child(session1)
    session2 = SessionNode(log_data["log3"]["session_id"])
    session2.duration = timedelta(hours=4, minutes=40, seconds=35)
    proj2.add_child(session2)
    log1 = LogNode(**log_data["log1"])
    log2 = LogNode(**log_data["log2"])
    session1.add_child(log1)
    session1.add_child(log2)
    log3 = LogNode(**log_data["log3"])
    log4 = LogNode(**log_data["log4"])
    session2.add_child(log3)
    session2.add_child(log4)

    node_dict = {
        "root": root,
        "project_node1": proj1,
        "session_node1": session1,
        "log_node1": log1,
        "log_node2": log2,
        "project_node2": proj2,
        "session_node2": session2,
        "log_node3": log3,
        "log_node4": log4,
    }
    return node_dict


@pytest.fixture
def queue_data(nodes):
    # Creating report components for Queue
    objs = list()
    report_head = ReportHeaderSummary(nodes["root"], REPORT_HEADER_FOOTER_FIELD_LAYOUTS[1])
    print(f'\nNode: {report_head.node}')
    report_head.compile_data()
    report_head.compile_report_header()
    objs.append(report_head)

    proj1 = Section(nodes["project_node1"], SECTION_FIELD_LAYOUTS[1])
    print(f'Node: {nodes["project_node1"]}')
    print(f'Node: {proj1.node}')
    proj1.compile_data()
    objs.append(proj1)

    session1 = Section(nodes["session_node1"], SECTION_FIELD_LAYOUTS[1])
    print(f'Node: {session1.node}')
    session1.compile_data()
    objs.append(session1)

    row1 = Row(nodes["log_node1"], ROW_FIELD_LAYOUTS[1])
    print(f'Node: {row1.node}')
    row1.compile_data()
    objs.append(row1)

    row2 = Row(nodes["log_node2"], ROW_FIELD_LAYOUTS[1])
    row2.compile_data()
    objs.append(row2)

    proj2 = Section(nodes["project_node2"], SECTION_FIELD_LAYOUTS[1])
    proj2.compile_data()
    objs.append(proj2)

    session2 = Section(nodes["session_node2"], SECTION_FIELD_LAYOUTS[1])
    session2.compile_data()
    objs.append(session2)

    row3 = Row(nodes["log_node3"], ROW_FIELD_LAYOUTS[1])
    row3.compile_data()
    objs.append(row3)

    row4 = Row(nodes["log_node4"], ROW_FIELD_LAYOUTS[1])
    row4.compile_data()
    objs.append(row4)

    return objs


def test_queue(queue_data):
    report = queue_data[0]
    assert isinstance(report, ReportHeaderSummary)
    assert report.data["reporting_on"] == 'projects 3 & 7'
