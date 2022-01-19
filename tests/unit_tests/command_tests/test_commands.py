import pytest
import datetime

from utils.command_enums import InputType


@pytest.fixture
def command_arg_input_full():
    arg_dict = {
        'time': datetime(2021, 1, 1, 12, 55, 40),
        'log_note': 'THIS IS A LOG NOTE',
        'project_name': 'Test',
        'session_note': 'THIS IS A SESSION NOTE'
    }
    return arg_dict


def test_START_command(command_arg_input_full):
    command = StartCommand(InputType.START, **command_arg_input_full)
    assert command.command == InputType.START
    assert command.get_command_name() == 'START'
    assert command.time == datetime(2021, 1, 1, 12, 55, 40)
    assert command.project_name == 'Test'
    assert command.last_command_log_note == 'THIS IS A LOG NOTE'
    assert command.session_note == 'THIS IS A SESSION NOTE'


def test_START_command_missing_optional_args():
    d = {'time': datetime(2021, 1, 1, 12, 55, 40)}
    command = StartCommand(InputType.START, **d)
    assert command.command == InputType.START
    assert command.get_command_name() == 'START'
    assert command.time == datetime(2021, 1, 1, 12, 55, 40)
    assert command.project_name is None
    assert command.last_command_log_note is None
    assert command.session_note is None


def test_START_command_sequence_validate(command_arg_input_full):
    command = StartCommand(InputType.START, **command_arg_input_full)
    with pytest.raises(Exception) as e:
        command.validate_sequence(InputType.PAUSE)
    with pytest.raises(Exception) as e:
        command.validate_sequence(InputType.START)
    with pytest.raises(Exception) as e:
        command.validate_sequence(InputType.RESUME)
    with pytest.raises(Exception) as e:
        command.validate_sequence(InputType.STOP)


def test_PAUSE_command(command_arg_input_full):
    command = PauseCommand(InputType.PAUSE, **command_arg_input_full)
    assert command.command == InputType.PAUSE
    assert command.get_command_name() == 'PAUSE'
    assert command.time == datetime(2021, 1, 1, 12, 55, 40)
    assert command.last_command_log_note == 'THIS IS A LOG NOTE'


def test_PAUSE_command_missing_optional_args():
    d = {'time': datetime(2021, 1, 1, 12, 55, 40)}
    command = PauseCommand(InputType.PAUSE, **d)
    assert command.command == InputType.PAUSE
    assert command.get_command_name() == 'PAUSE'
    assert command.time == datetime(2021, 1, 1, 12, 55, 40)
    assert command.last_command_log_note is None


def test_PAUSE_command_ignores_unallowed_attr(command_arg_input_full):
    command = PauseCommand(InputType.PAUSE, **command_arg_input_full)
    assert command.command == InputType.PAUSE
    assert command.get_command_name() == 'PAUSE'
    assert command.time == datetime(2021, 1, 1, 12, 55, 40)
    assert command.last_command_log_note == 'THIS IS A LOG NOTE'
    with pytest.raises(AttributeError):
        command.session_note
    with pytest.raises(AttributeError):
        command.project_name


def test_PAUSE_command_sequence_validate(command_arg_input_full):
    # Todo: This test is not creating errors when it should
    command = PauseCommand(InputType.PAUSE, **command_arg_input_full)
    with pytest.raises(Exception) as e:
        command.validate_sequence(InputType.PAUSE)
    with pytest.raises(Exception) as e:
        command.validate_sequence(InputType.START)
    with pytest.raises(Exception) as e:
        command.validate_sequence(InputType.RESUME)
    with pytest.raises(Exception) as e:
        command.validate_sequence(InputType.STOP)


def test_RESUME_command(command_arg_input_full):
    command = ResumeCommand(InputType.RESUME, **command_arg_input_full)
    assert command.command == InputType.RESUME
    assert command.get_command_name() == 'RESUME'
    assert command.time == datetime(2021, 1, 1, 12, 55, 40)
    assert command.last_command_log_note == 'THIS IS A LOG NOTE'


def test_RESUME_command_missing_optional_args():
    d = {'time': datetime(2021, 1, 1, 12, 55, 40)}
    command = ResumeCommand(InputType.RESUME, **d)
    assert command.command == InputType.RESUME
    assert command.get_command_name() == 'RESUME'
    assert command.time == datetime(2021, 1, 1, 12, 55, 40)
    assert command.last_command_log_note is None


def test_RESUME_command_ignores_unallowed_attr(command_arg_input_full):
    command = ResumeCommand(InputType.RESUME, **command_arg_input_full)
    assert command.command == InputType.RESUME
    assert command.get_command_name() == 'RESUME'
    assert command.time == datetime(2021, 1, 1, 12, 55, 40)
    assert command.last_command_log_note == 'THIS IS A LOG NOTE'
    with pytest.raises(AttributeError):
        command.session_note
    with pytest.raises(AttributeError):
        command.project_name


def test_RESUME_command_sequence_validate(command_arg_input_full):
    # Todo: This test is not creating errors when it should
    command = ResumeCommand(InputType.RESUME, **command_arg_input_full)
    with pytest.raises(Exception) as e:
        command.validate_sequence(InputType.START)
    with pytest.raises(Exception) as e:
        command.validate_sequence(InputType.RESUME)


@pytest.fixture
def command_arg_input_utility_commands():
    arg_dict = {
        'all': True,
        'project_name': 'Test',
        'project_id': 456,
        'filter_by': 1
    }
    return arg_dict


def test_STATUS_command(command_arg_input_utility_commands):
    command = StatusCheck(InputType.STATUS, **command_arg_input_utility_commands)
    assert command.is_all() is True
    assert command.get_command_name() == 'STATUS'
    assert command.command == InputType.STATUS
    with pytest.raises(AttributeError):
        command.project_name
    with pytest.raises(AttributeError):
        command.project_id


def test_PROJECTS_command(command_arg_input_utility_commands):
    command = ProjectsCommand(InputType.PROJECTS, **command_arg_input_utility_commands)
    assert command.project_name == 'Test'
    assert command.is_all() is True
    assert command.filter_by == 1
    assert command.get_command_name() == 'PROJECTS'
    assert command.command == InputType.PROJECTS
    with pytest.raises(AttributeError):
        command.project_id


def test_NEW_command(command_arg_input_utility_commands):
    command = NewCommand(InputType.NEW, **command_arg_input_utility_commands)
    assert command.project_name == 'Test'
    assert command.get_command_name() == 'NEW'
    assert command.command == InputType.NEW
    with pytest.raises(AttributeError):
        command.all
    with pytest.raises(AttributeError):
        command.project_id


def test_FETCH_command(command_arg_input_utility_commands):
    command = FetchProject(InputType.FETCH, **command_arg_input_utility_commands)
    assert command.project_id == 456
    assert command.get_command_name() == 'FETCH'
    assert command.command == InputType.FETCH
    with pytest.raises(AttributeError):
        command.all
    with pytest.raises(AttributeError):
        command.project_name


def test_SWITCH_command(command_arg_input_utility_commands):
    command = SwitchCommand(InputType.SWITCH, **command_arg_input_utility_commands)
    assert command.project_id == 456
    assert command.get_command_name() == 'SWITCH'
    assert command.command == InputType.SWITCH
    with pytest.raises(AttributeError):
        command.all
    with pytest.raises(AttributeError):
        command.project_name
