import pytest
from pytest_mock import mocker

from utils.command_enums import InputType
from timer_session.session_datetime_converter import DateTimeConverter

# Objects for testing
from timer_session.sessions_manager import create_session
from timer_session.sessions_manager import convert_data_for_session_object
from timer_session.sessions_manager import start_manager
from timer_session.session import Session


@pytest.fixture
def json_data_multiple_sessions():
    data = [
        {
            "project_name": "world",
            "project_id": 7,
            "last_command": "NO_SESSION",
            "session_id": 66,
            "session_start_time": "None",
            "last_command_time": "None",
            "last_command_log_note": "None",
            "current_session": "False"
        },
        {
            "project_name": "hello",
            "project_id": 3,
            "last_command": "PAUSE",
            "session_id": 124,
            "session_start_time": "10/05/21_15:12:37",
            "last_command_time": "10/05/21_19:24:52",
            "last_command_log_note": "Gotta use the restroom",
            "current_session": "False"
        },
        {
            "project_name": "pony",
            "project_id": 15,
            "last_command": "RESUME",
            "session_id": 123,
            "session_start_time": "10/06/21_09:12:28",
            "last_command_time": "10/06/21_22:10:43",
            "last_command_log_note": "Gotta finish this by midnight",
            "current_session": "True"
        }

    ]
    return data


@pytest.fixture
def json_data_one_session():
    data = [
        {
            "project_name": "pony",
            "project_id": 15,
            "last_command": "RESUME",
            "session_id": 123,
            "session_start_time": "10/06/21_09:12:28",
            "last_command_time": "10/06/21_22:10:43",
            "last_command_log_note": "Gotta finish this by midnight",
            "current_session": "True"
        }
    ]
    return data


def test_convert_data_for_session_object(json_data_one_session):
    data = convert_data_for_session_object(json_data_one_session[0])
    assert data["project_name"] == 'pony'
    assert data["project_id"] == 15
    assert data["last_command"] == InputType.RESUME
    assert data["session_id"] == 123
    assert data["session_start_time"] == DateTimeConverter("10/06/21_09:12:28").get_datetime_obj()
    assert data["last_command_time"] == DateTimeConverter("10/06/21_22:10:43").get_datetime_obj()
    assert data["last_command_log_note"] == "Gotta finish this by midnight"
    assert data["current_session"] is True


def test_create_session(json_data_one_session):
    data = convert_data_for_session_object(json_data_one_session[0])
    session = create_session(data)
    assert session.project_name == 'pony'
    assert session.project_id == 15
    assert session.last_command == InputType.RESUME
    assert session.session_id == 123
    assert session.session_start_time == DateTimeConverter("10/06/21_09:12:28").get_datetime_obj()
    assert session.last_command_time == DateTimeConverter("10/06/21_22:10:43").get_datetime_obj()
    assert session.last_command_log_note == "Gotta finish this by midnight"
    assert session.current_session is True


def test_start_manager(mocker, json_data_multiple_sessions):
    mocker.patch('timer_session.sessions_manager.load_session', return_value=json_data_multiple_sessions)
    manager = start_manager()
    assert len(manager.sessions) == 3


def test_start_manager_remove_session(mocker, json_data_multiple_sessions):
    mocker.patch('timer_session.sessions_manager.load_session', return_value=json_data_multiple_sessions)
    manager = start_manager()
    assert len(manager.sessions) == 3
    manager.remove_session(3)
    assert len(manager.sessions) == 2


def test_start_manager_assign_current(mocker, json_data_multiple_sessions):
    mocker.patch('timer_session.sessions_manager.load_session', return_value=json_data_multiple_sessions)
    manager = start_manager()
    manager.remove_session(3)
    assert len(manager.sessions) == 2

# Todo: Test that config settings work

"""
def test_session_with_data(mocker, json_data):
    mocker.patch('timer_session.timer_session.Session._load_json_file', return_value=json_data)
    session = CurrentSession()
    assert session.project_name() == 'Test Project'
    assert session.session_start_time() == DateTimeCreator('10/05/21_15:12:37').get_dt_obj()
    assert session.get_last_command() == 'PAUSE'
    assert session.last_command() == InputType.PAUSE
    assert session.last_command_time() == DateTimeCreator('10/10/21_08:44:51').get_dt_obj()
    assert len(session.get_time_log()) == 4


@pytest.fixture
def json_data_blank_session():
    data = {
            "last_command": "NO_SESSION",
            "project_name": "None",
            "time_log": []
        }
    return data


def test_session_no_data(mocker, json_data_blank_session):
    mocker.patch('timer_session.timer_session.Session._load_json_file', return_value=json_data_blank_session)
    session = CurrentSession()
    assert session.project_name() == 'None'
    assert session.session_start_time() is None
    assert session.get_last_command() == 'NO_SESSION'
    assert session.last_command() == InputType.NO_SESSION
    assert session.last_command_time() is None
    assert len(session.get_time_log()) == 0


def test_session_add_time_no_data(mocker, json_data_blank_session):
    mocker.patch('timer_session.timer_session.Session._load_json_file', return_value=json_data_blank_session)
    session = CurrentSession()
    new_time = DateTimeCreator('10/12/21_05:05:05').get_dt_obj()
    session.add_time_entry(new_time)
    assert session.session_start_time() == new_time
    assert session.last_command_time() == new_time
    assert len(session.get_time_log()) == 1


@pytest.fixture
def json_data_one_time():
    data = {
            "last_command": "PAUSE",
            "project_name": "Test Time",
            "time_log": [['10/05/21_15:12:37']]
        }
    return data


def test_session_with_one_time_entry(mocker, json_data_one_time):
    mocker.patch('timer_session.timer_session.Session._load_json_file', return_value=json_data_one_time)
    session = CurrentSession()
    assert session.session_start_time() == DateTimeCreator('10/05/21_15:12:37').get_dt_obj()
    assert session.last_command_time() == DateTimeCreator('10/05/21_15:12:37').get_dt_obj()
    assert len(session.get_time_log()) == 1


def test_session_time_add_with_one_time_entry(mocker, json_data_one_time):
    mocker.patch('timer_session.timer_session.Session._load_json_file', return_value=json_data_one_time)
    session = CurrentSession()
    new_time = DateTimeCreator('10/12/21_05:05:05').get_dt_obj()
    session.add_time_entry(new_time)
    assert session.session_start_time() == DateTimeCreator('10/05/21_15:12:37').get_dt_obj()
    assert session.last_command_time() == new_time
    assert len(session.get_time_log()) == 1


@pytest.fixture
def json_data_two_times():
    data = {
            "last_command": "PAUSE",
            "project_name": "Test Time",
            "time_log": [['10/05/21_15:12:37', '10/05/21_17:12:19']]
        }
    return data


def test_session_time_add_with_two_time_entries(mocker, json_data_two_times):
    mocker.patch('timer_session.timer_session.Session._load_json_file', return_value=json_data_two_times)
    session = CurrentSession()
    new_time = DateTimeCreator('10/12/21_05:05:05').get_dt_obj()
    session.add_time_entry(new_time)
    assert session.session_start_time() == DateTimeCreator('10/05/21_15:12:37').get_dt_obj()
    assert session.last_command_time() == new_time
    assert len(session.get_time_log()) == 2
"""
