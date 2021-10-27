import pytest
import datetime
from timer_logic.commands import *
from utils.command_enums import InputType


def test_START_command():
    command = InputType.START
    time = datetime.datetime(2021, 1, 1, 12, 55, 40)
    name = 'Test'
    command = StartCommand(command, name, time)
    assert command.get_command_type() == InputType.START
    assert command.get_command_name() == 'START'
    assert datetime.datetime(2021, 1, 1, 12, 55, 40) == datetime.datetime(2021, 1, 1, 12, 55, 40)
    assert command.get_project_name() == 'Test'


def test_START_command_sequence_validate():
    command = InputType.START
    time = datetime.datetime(2021, 1, 1, 12, 55, 40)
    name = 'Test'
    command = StartCommand(command, name, time)
    with pytest.raises(Exception) as e:
        command.validate_sequence(InputType.PAUSE)
    with pytest.raises(Exception) as e:
        command.validate_sequence(InputType.START)
    with pytest.raises(Exception) as e:
        command.validate_sequence(InputType.RESUME)
    with pytest.raises(Exception) as e:
        command.validate_sequence(InputType.STOP)


def test_PAUSE_command_sequence_validate():
    # Todo: This test is not creating errors when it should
    command = InputType.PAUSE
    time = datetime.datetime(2021, 1, 1, 12, 55, 40)
    command = PauseCommand(command, time)
    with pytest.raises(Exception) as e:
        command.validate_sequence(InputType.PAUSE)
    with pytest.raises(Exception) as e:
        command.validate_sequence(InputType.START)
    with pytest.raises(Exception) as e:
        command.validate_sequence(InputType.RESUME)
    with pytest.raises(Exception) as e:
        command.validate_sequence(InputType.STOP)


def test_RESUME_command_sequence_validate():
    # Todo: This test is not creating errors when it should
    command = InputType.RESUME
    time = datetime.datetime(2021, 1, 1, 12, 55, 40)
    command = ResumeCommand(command, time)
    with pytest.raises(Exception) as e:
        command.validate_sequence(InputType.START)
    with pytest.raises(Exception) as e:
        command.validate_sequence(InputType.RESUME)


def test_FETCH_command():
    project_id = 123
    command = FetchProject(InputType.FETCH, project_id)
    assert command.get_project_id() == project_id
    assert command.get_command_name() == 'FETCH'


def test_NEW_command():
    project_name = 'Fish'
    command = NewCommand(InputType.NEW, project_name)
    assert command.get_project_name() == project_name
    assert command.get_command_name() == 'NEW'

