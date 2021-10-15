import pytest
import datetime
from handlers.commands import *
from utils.command_enums import InputType


@pytest.fixture
def time_object():
    date = datetime.date.today()
    return datetime.datetime(date.year, date.month, date.day, hour=13, minute=55)

def test_STARTcommand_without_time():
    s = InputType.START
    command = StartCommand(s, 'Test')
    assert command.get_command_type() == InputType.START
    assert type(command.get_command_time()) == datetime.datetime
    assert command.get_project_name() == 'Test'


def test_STARTcommand_time(time_object):
    s = InputType.START
    command = StartCommand(s, 'Test', '1355')
    assert command.get_command_type() == InputType.START
    assert type(command.get_command_time()) == time_object
    assert command.get_project_name() == 'Test'
