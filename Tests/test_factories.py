import pytest
import pytest_mock
import datetime

from timer_logic.command_factories import LogCommandFactory, StatusMiscCommandFactory, command_factory_router
from utils.command_enums import InputType
from timer import LogArgs, StatusMiscArgs


@pytest.fixture
def log_args():
    time = datetime.datetime(2021, 10, 20, 5, 14, 33)
    name = None
    return LogArgs(time=time, name=name)


def test_log_factory_PAUSE(log_args):
    command = InputType.PAUSE
    command_dict = {'command': command, 'command_args': log_args}
    command_obj = LogCommandFactory(command_dict).create_command()
    assert command_obj.get_command_type() == InputType.PAUSE
    assert command_obj.get_command_name() == 'PAUSE'
    assert command_obj.get_command_time() == datetime.datetime(2021, 10, 20, 5, 14, 33)


@pytest.fixture
def start_args():
    args = LogArgs(time=datetime.datetime(2021, 10, 20, 5, 14, 33), name="Fancy Pants Test")
    command = InputType.START
    return {'command': command, 'command_args': args}


def test_log_factory_START(start_args):
    command_obj = LogCommandFactory(start_args).create_command()
    assert command_obj.get_command_type() == InputType.START
    assert command_obj.get_command_name() == 'START'
    assert command_obj.get_command_time() == datetime.datetime(2021, 10, 20, 5, 14, 33)
    assert command_obj.get_project_name() == 'Fancy Pants Test'


@pytest.fixture
def fetch_data():
    command = InputType.FETCH
    args = StatusMiscArgs(project_id=1)
    return {'command': command, 'command_args': args}


def test_fetch_project(fetch_data):
    command_obj = StatusMiscCommandFactory(fetch_data).create_command()
    assert command_obj.get_project_id() == 1
    assert command_obj.get_command_name() == 'FETCH'
    assert command_obj.get_command_type() == InputType.FETCH


def test_command_factory_router_START(start_args):
    command_obj = command_factory_router(start_args)
    assert command_obj.get_command_type() == InputType.START
    assert command_obj.get_command_name() == 'START'
    assert command_obj.get_command_time() == datetime.datetime(2021, 10, 20, 5, 14, 33)
    assert command_obj.get_project_name() == 'Fancy Pants Test'


def test_command_factory_router_FETCH(fetch_data):
    command_obj = command_factory_router(fetch_data)
    assert command_obj.get_project_id() == 1
    assert command_obj.get_command_name() == 'FETCH'
    assert command_obj.get_command_type() == InputType.FETCH
