import pytest
import pytest_mock

from timer_session.timer_session import Session
from utils.command_enums import InputType

from timer_session.timer_session import DateTimeConverter  # Using to create dt object


@pytest.fixture
def json_data():
    data = {
            "last_command": "PAUSE",
            "project_name": "Test Project",
            "time_log": [
                ['10/05/21_15:12:37', '10/05/21_17:12:19'],
                ['10/06/21_09:12:28', '10/06/21_09:33:20'],
                ['10/07/21_11:12:18', '10/07/21_15:34:00'],
                ['10/10/21_07:12:13', '10/10/21_08:44:51']
            ]
        }
    return data


def test_session_with_data(mocker, json_data):
    mocker.patch('timer_session.timer_session.Session._load_json_file', return_value=json_data)
    session = Session()
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
    session = Session()
    assert session.project_name() == 'None'
    assert session.session_start_time() is None
    assert session.get_last_command() == 'NO_SESSION'
    assert session.last_command() == InputType.NO_SESSION
    assert session.last_command_time() is None
    assert len(session.get_time_log()) == 0


def test_session_add_time_no_data(mocker, json_data_blank_session):
    mocker.patch('timer_session.timer_session.Session._load_json_file', return_value=json_data_blank_session)
    session = Session()
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
    session = Session()
    assert session.session_start_time() == DateTimeCreator('10/05/21_15:12:37').get_dt_obj()
    assert session.last_command_time() == DateTimeCreator('10/05/21_15:12:37').get_dt_obj()
    assert len(session.get_time_log()) == 1


def test_session_time_add_with_one_time_entry(mocker, json_data_one_time):
    mocker.patch('timer_session.timer_session.Session._load_json_file', return_value=json_data_one_time)
    session = Session()
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
    session = Session()
    new_time = DateTimeCreator('10/12/21_05:05:05').get_dt_obj()
    session.add_time_entry(new_time)
    assert session.session_start_time() == DateTimeCreator('10/05/21_15:12:37').get_dt_obj()
    assert session.last_command_time() == new_time
    assert len(session.get_time_log()) == 2
