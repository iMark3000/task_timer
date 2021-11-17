import pytest
from datetime import datetime

from timer_logic.factories.utility_command_factory import UtilityCommandFactory
from timer_logic.factories.log_command_factory import LogCommandFactory
from timer_logic.factories.config_command_factory import ConfigCommandFactory
from timer_logic.factories.factory_router import command_factory_router

from utils.command_enums import InputType


@pytest.fixture
def log_args():
    arg_dict = {
        'time': datetime(2021, 1, 1, 12, 55, 40),
        'log_note': 'THIS IS A LOG NOTE',
        'project_name': 'Test',
        'session_note': 'THIS IS A SESSION NOTE'
    }
    return arg_dict


def test_log_factory_PAUSE(log_args):
    command = InputType.PAUSE
    command_obj = LogCommandFactory(command, log_args).create_command()
    assert command_obj.command == InputType.PAUSE
    assert command_obj.get_command_name() == 'PAUSE'
    assert command_obj.time == datetime(2021, 1, 1, 12, 55, 40)
    assert command_obj.last_command_log_note == 'THIS IS A LOG NOTE'
    with pytest.raises(AttributeError):
        command.session_note
    with pytest.raises(AttributeError):
        command.project_name


def test_log_factory_RESUME(log_args):
    command = InputType.RESUME
    command_obj = LogCommandFactory(command, log_args).create_command()
    assert command_obj.command == InputType.RESUME
    assert command_obj.get_command_name() == 'RESUME'
    assert command_obj.time == datetime(2021, 1, 1, 12, 55, 40)
    assert command_obj.last_command_log_note == 'THIS IS A LOG NOTE'
    with pytest.raises(AttributeError):
        command.session_note
    with pytest.raises(AttributeError):
        command.project_name


def test_log_factory_STOP(log_args):
    command = InputType.STOP
    command_obj = LogCommandFactory(command, log_args).create_command()
    assert command_obj.command == InputType.STOP
    assert command_obj.get_command_name() == 'STOP'
    assert command_obj.time == datetime(2021, 1, 1, 12, 55, 40)
    assert command_obj.last_command_log_note == 'THIS IS A LOG NOTE'
    with pytest.raises(AttributeError):
        command.session_note
    with pytest.raises(AttributeError):
        command.project_name


def test_log_factory_START(log_args):
    command_obj = LogCommandFactory(InputType.START, log_args).create_command()
    assert command_obj.command == InputType.START
    assert command_obj.get_command_name() == 'START'
    assert command_obj.time == datetime(2021, 1, 1, 12, 55, 40)
    assert command_obj.project_name == 'Test'
    assert command_obj.last_command_log_note == 'THIS IS A LOG NOTE'
    assert command_obj.session_note == 'THIS IS A SESSION NOTE'


# ~~~~~~~~~~~~TESTS FOR UTILITY FACTORY~~~~~~~~~~~~


@pytest.fixture
def utility_factory_input():
    arg_dict = {
        'all': True,
        'project_name': 'Test',
        'project_id': 456
    }
    return arg_dict


def test_STATUS_project(utility_factory_input):
    command = UtilityCommandFactory(InputType.STATUS, utility_factory_input).create_command()
    assert command.is_all() is True
    assert command.get_command_name() == 'STATUS'
    assert command.command == InputType.STATUS
    with pytest.raises(AttributeError):
        command.project_name
    with pytest.raises(AttributeError):
        command.project_id


def test_PROJECTS_project(utility_factory_input):
    command = UtilityCommandFactory(InputType.PROJECTS, utility_factory_input).create_command()
    assert command.project_name == 'Test'
    assert command.is_all() is True
    assert command.get_command_name() == 'PROJECTS'
    assert command.command == InputType.PROJECTS
    with pytest.raises(AttributeError):
        command.project_id


def test_NEW_project(utility_factory_input):
    command = UtilityCommandFactory(InputType.NEW, utility_factory_input).create_command()
    assert command.project_name == 'Test'
    assert command.get_command_name() == 'NEW'
    assert command.command == InputType.NEW
    with pytest.raises(AttributeError):
        command.all
    with pytest.raises(AttributeError):
        command.project_id


def test_fetch_project(utility_factory_input):
    command = UtilityCommandFactory(InputType.FETCH, utility_factory_input).create_command()
    assert command.project_id == 456
    assert command.get_command_name() == 'FETCH'
    assert command.command == InputType.FETCH
    with pytest.raises(AttributeError):
        command.all
    with pytest.raises(AttributeError):
        command.project_name


def test_SWITCH_project(utility_factory_input):
    command = UtilityCommandFactory(InputType.SWITCH, utility_factory_input).create_command()
    assert command.project_id == 456
    assert command.get_command_name() == 'SWITCH'
    assert command.command == InputType.SWITCH
    with pytest.raises(AttributeError):
        command.all
    with pytest.raises(AttributeError):
        command.project_name


# ~~~~~~~~~~~~TESTS FOR FACTORY ROUTER FUNCTION~~~~~~~~~~~~


def test_command_factory_router_START(log_args):
    args = (InputType.START, log_args)
    command_obj = command_factory_router(args)
    assert command_obj.command == InputType.START
    assert command_obj.get_command_name() == 'START'
    assert command_obj.time == datetime(2021, 1, 1, 12, 55, 40)
    assert command_obj.project_name == 'Test'
    assert command_obj.last_command_log_note == 'THIS IS A LOG NOTE'
    assert command_obj.session_note == 'THIS IS A SESSION NOTE'


def test_command_factory_router_PAUSE(log_args):
    args = (InputType.PAUSE, log_args)
    command_obj = command_factory_router(args)
    assert command_obj.command == InputType.PAUSE
    assert command_obj.get_command_name() == 'PAUSE'
    assert command_obj.time == datetime(2021, 1, 1, 12, 55, 40)
    assert command_obj.last_command_log_note == 'THIS IS A LOG NOTE'
    with pytest.raises(AttributeError):
        command_obj.session_note
    with pytest.raises(AttributeError):
        command_obj.project_name


def test_command_factory_router_RESUME(log_args):
    args = (InputType.RESUME, log_args)
    command_obj = command_factory_router(args)
    assert command_obj.command == InputType.RESUME
    assert command_obj.get_command_name() == 'RESUME'
    assert command_obj.time == datetime(2021, 1, 1, 12, 55, 40)
    assert command_obj.last_command_log_note == 'THIS IS A LOG NOTE'
    with pytest.raises(AttributeError):
        command_obj.session_note
    with pytest.raises(AttributeError):
        command_obj.project_name


def test_command_factory_router_STOP(log_args):
    args = (InputType.STOP, log_args)
    command_obj = command_factory_router(args)
    assert command_obj.command == InputType.STOP
    assert command_obj.get_command_name() == 'STOP'
    assert command_obj.time == datetime(2021, 1, 1, 12, 55, 40)
    assert command_obj.last_command_log_note == 'THIS IS A LOG NOTE'
    with pytest.raises(AttributeError):
        command_obj.session_note
    with pytest.raises(AttributeError):
        command_obj.project_name


def test_command_factory_router_FETCH(fetch_data):
    command_obj = command_factory_router(fetch_data)
    assert command_obj.project_id() == 1
    assert command_obj.get_command_name() == 'FETCH'
    assert command_obj.get_command_type() == InputType.FETCH

