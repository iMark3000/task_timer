import pytest
import pprint
from datetime import date

from src.command_classes.commands import QueryCommand
from src.utils.command_enums import InputType
from src.timer_logic.handlers.query_command_handler import QueryCommandHandler


@pytest.fixture
def create_command():
    return QueryCommand(InputType.QUERY)


@pytest.fixture
def create_project_query():
    return [{'project_id': 1, 'project_name': 'air bud'},
            {'project_id': 2, 'project_name': 'milo and ottis'}]


@pytest.fixture
def create_session_query():
    return [{'session_id': 1, 'project_id': 1, 'note': None},
            {'session_id': 2, 'project_id': 2, 'note': None},
            {'session_id': 3, 'project_id': 1, 'note': None}]


@pytest.fixture
def create_log_query():
    return [
        {'end_note': None,
         'end_timestamp': '2022-01-01 10:30:00',
         'log_id': 1,
         'session_id': 1,
         'start_note': None,
         'start_timestamp': '2022-01-01 10:00:00'},
        {'end_note': None,
         'end_timestamp': '2022-01-01 10:40:00',
         'log_id': 2,
         'session_id': 1,
         'start_note': None,
         'start_timestamp': '2022-01-01 10:35:00'},
        {'end_note': None,
         'end_timestamp': '2022-01-01 13:25:00',
         'log_id': 3,
         'session_id': 2,
         'start_note': None,
         'start_timestamp': '2022-01-01 13:00:00'},
        {'end_note': None,
         'end_timestamp': '2022-01-01 13:50:00',
         'log_id': 4,
         'session_id': 2,
         'start_note': None,
         'start_timestamp': '2022-01-01 13:44:00'}
    ]


@pytest.fixture
def create_session_project_combined_query():
    return [
        {'note': None, 'project_id': 1, 'project_name': 'air bud', 'session_id': 1},
        {'note': None, 'project_id': 1, 'project_name': 'air bud', 'session_id': 3},
        {'note': None, 'project_id': 2, 'project_name': 'milo and ottis', 'session_id': 2}]


@pytest.fixture
def create_log_session_combined_query():
    return [
        {'end_note': None,
         'end_timestamp': '2022-01-01 10:30:00',
         'log_id': 1,
         'note': None,
         'project_id': 1,
         'project_name': 'air bud',
         'session_id': 1,
         'start_note': None,
         'start_timestamp': '2022-01-01 10:00:00'},
        {'end_note': None,
         'end_timestamp': '2022-01-01 10:40:00',
         'log_id': 2,
         'note': None,
         'project_id': 1,
         'project_name': 'air bud',
         'session_id': 1,
         'start_note': None,
         'start_timestamp': '2022-01-01 10:35:00'},
        {'end_note': None,
         'end_timestamp': '2022-01-01 13:25:00',
         'log_id': 3,
         'note': None,
         'project_id': 2,
         'project_name': 'milo and ottis',
         'session_id': 2,
         'start_note': None,
         'start_timestamp': '2022-01-01 13:00:00'},
        {'end_note': None,
         'end_timestamp': '2022-01-01 13:50:00',
         'log_id': 4,
         'note': None,
         'project_id': 2,
         'project_name': 'milo and ottis',
         'session_id': 2,
         'start_note': None,
         'start_timestamp': '2022-01-01 13:44:00'}
    ]


def test_combine_queries_project_to_session(create_project_query, create_session_query, create_command):
    handler = QueryCommandHandler(create_command)
    result = handler.combine_queries(create_project_query, create_session_query)
    print('\n')
    pprint.pprint(result)


def test_combine_queries_log_to_session_projects(create_log_query, create_session_project_combined_query, create_command):
    handler = QueryCommandHandler(create_command)
    result = handler.combine_queries(create_log_query, create_session_project_combined_query)
    print('\n')
    pprint.pprint(result)


def test_combine_queries_session_to_log(create_log_query, create_session_query, create_command):
    handler = QueryCommandHandler(create_command)
    result = handler.combine_queries(create_session_query, create_log_query)
    print('\n')
    pprint.pprint(result)


def test_combine_queries_projects_to_session_log(create_project_query, create_log_session_combined_query, create_command):
    handler = QueryCommandHandler(create_command)
    result = handler.combine_queries(create_project_query, create_log_session_combined_query)
    print('\n')
    pprint.pprint(result)


@pytest.fixture
def create_query_command():
    tup = (InputType.QUERY,
           {'query_projects': (123,),
            'query_level': 1,
            'end_date': date(year=2022, month=1, day=12),
            'start_date': date(year=2021, month=10, day=15),
            'query_time_period': 'CY'}
           )
    return QueryCommand(tup[0], **tup[1])


def test_create__create_time_stamps_for_query_time_period(create_query_command):
    handler = QueryCommandHandler(create_query_command)
    result = handler._create_time_stamps_for_query_time_period()
    print(result)


def test_process_queries_top_down(create_query_command):
    pids = (1, 2)
    d = {"start_date": create_query_command.start_date, "end_date": create_query_command.end_date}
    handler = QueryCommandHandler(create_query_command)
    result = handler._process_queries_top_down(pids, d)
    pprint.pprint(result)


def test_process_queries_bottom_up(create_query_command):
    d = {"start_date": create_query_command.start_date, "end_date": create_query_command.end_date}
    handler = QueryCommandHandler(create_query_command)
    result = handler._process_queries_bottom_up(d)
    pprint.pprint(result)