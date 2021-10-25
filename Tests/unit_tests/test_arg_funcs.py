import pytest
import datetime

from timer import arg_parser, arg_named_tuple
from timer import LogArgs
from utils.command_enums import InputType


@pytest.fixture
def pause_command_data_with_time():
    pass


@pytest.fixture
def pause_command_data_without_time():
    pass


@pytest.fixture
def start_command_data_with_time():
    command = InputType.START
    command_args = ['Test', '1632']
    return command, command_args

@pytest.fixture
def start_command_data_without_time():
    pass


def test_arg_named_tuple_start_without_time():
    pass


def test_arg_named_tuple_start_with_time(start_command_data_with_time):
    func = arg_named_tuple(start_command_data_with_time[0], start_command_data_with_time[1])
    today = datetime.date.today()
    expected_time = datetime.datetime(today.year, today.month, today.day, hour=16, minute=32)
    assert type(func) == LogArgs
    assert func.time == expected_time
    assert func.name == 'Test'


def test_arg_named_tuple_pause_without_time():
    pass


def test_arg_named_tuple_pause_with_time():
    pass


@pytest.fixture
def fetch_command_data():
    pass


def test_arg_named_tuple_fetch():
    pass
