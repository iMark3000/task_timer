import pytest
from datetime import timedelta
from datetime import datetime

from timer_reports.report_tree.report_nodes import RootNode
from timer_reports.report_tree.report_nodes import ProjectNode
from timer_reports.report_tree.report_nodes import SessionNode
from timer_reports.report_tree.report_nodes import LogNode

from timer_reports.layout.report_componenets import ReportHeaderSummary
from timer_reports.layout.report_componenets import Section
from timer_reports.layout.report_componenets import Row

# create nodes
# create components

@pytest.fixture
def log_data():
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
def nodes(data):
    root = RootNode('projects 3 & 7', '11/17/2021 to 11/21/2021')
    proj1 = ProjectNode(**data["log1"]["project_id"], **data["log3"]["project_name"])
    proj2 = ProjectNode(**data["log3"]["project_id"], **data["log3"]["project_name"])
    session1 = SessionNode(**data["log1"]["session_id"])
    session2 = SessionNode(**data["log3"]["session_id"])
    log1 = LogNode(**data["log1"])
    log2 = LogNode(**data["log2"])
    log3 = LogNode(**data["log3"])
    log4 = LogNode(**data["log4"])

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


@pytest.fixture
def queue_data():
    objs = [
        ReportHeaderSummary(),
        Section(),
        Section(),
        Row(),
        Row(),
        Section(),
        Section(),
        Row(),
        Row(),
        Row(),
    ]



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
