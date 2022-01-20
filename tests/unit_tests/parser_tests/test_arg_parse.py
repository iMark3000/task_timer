import pytest
import datetime

from src.timer_logic.arg_parsers.log_parse import LogCommandArgParser
from src.timer_logic.arg_parsers.log_parse import StartCommandArgParser
from src.timer_logic.arg_parsers.utility_parse import UtilityCommandArgParser
from src.timer_logic.arg_parsers.arg_parser_router import arg_router
from src.utils.command_enums import InputType

from src.utils.exceptions import RequiredArgMissing
from src.utils.exceptions import InvalidArgument
from src.utils.exceptions import TooManyCommandArgs


@pytest.fixture
def date_and_time():
    time = '1322'
    date = '3/24'
    return [time, date]


def test_LogCommandParser_time_date(date_and_time):
    command = InputType.PAUSE
    result = LogCommandArgParser(command, date_and_time).parse()
    assert result['command_args'].time == datetime.datetime(2021, 3, 24, hour=13, minute=22)


def test_LogCommandParser_time_no_date():
    command = InputType.PAUSE
    time = '1322'
    year = datetime.date.today().year
    month = datetime.date.today().month
    day = datetime.date.today().day
    args = [time]
    result = LogCommandArgParser(command, args).parse()
    assert result['command_args'].time == datetime.datetime(year, month, day, hour=13, minute=22)


def test_LogCommandParser_no_time_date():
    command = InputType.PAUSE
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    args = []
    result = LogCommandArgParser(command, args).parse()
    # str format to set seconds to "00"
    expected = datetime.datetime(year, month, day, hour=hour, minute=minute).strftime('%x %H:%M:00')
    assert result['command_args'].time.strftime('%x %H:%M:00') == expected


def test_StartCommandParser_time_date_name(date_and_time):
    command = InputType.START
    name = 'test'
    date_and_time.append(name)
    result = StartCommandArgParser(command, date_and_time).parse()
    assert result['command_args'].time == datetime.datetime(2021, 3, 24, hour=13, minute=22)
    assert result['command_args'].name == 'test'


def test_StatusMiscParser_FETCH():
    command = InputType.FETCH
    project_id = '1234'
    args = [project_id]
    result = UtilityCommandArgParser(command, args).parse()
    assert result['command_args'].project_id == int(project_id)


def test_arg_router_START(date_and_time):
    command = InputType.START
    name = 'Test'
    date_and_time.append(name)
    result = arg_router(command, date_and_time)
    assert result['command_args'].time == datetime.datetime(2021, 3, 24, hour=13, minute=22)


def test_arg_router_STOP(date_and_time):
    command = InputType.STOP
    result = arg_router(command, date_and_time)
    assert result['command_args'].time == datetime.datetime(2021, 3, 24, hour=13, minute=22)


def test_arg_router_STATUS():
    command = InputType.STATUS
    args = []
    result = arg_router(command, args)
    assert result['command_args'].project_id is None


def test_arg_router_STATUS_raise_err():
    command = InputType.STATUS
    args = ['hamburger']
    with pytest.raises(TooManyCommandArgs) as e:
        arg_router(command, args)


def test_arg_router_FETCH():
    command = InputType.FETCH
    args = ['123']
    result = arg_router(command, args)
    assert result['command_args'].project_id == 123


def test_arg_router_FETCH_raise_invalidarg_err():
    command = InputType.FETCH
    args = ['hamburger']
    with pytest.raises(InvalidArgument) as e:
        arg_router(command, args)


def test_arg_router_FETCH_raise_req_arg_missing_err():
    command = InputType.FETCH
    args = []
    with pytest.raises(RequiredArgMissing) as e:
        arg_router(command, args)


def test_arg_router_NEW():
    command = InputType.NEW
    args = ['Cat12']
    result = arg_router(command, args)
    assert result['command_args'].project_name == 'Cat12'


def test_arg_router_NEW_raise_invalidarg_err():
    command = InputType.NEW
    args = ['hi']
    with pytest.raises(InvalidArgument) as e:
        arg_router(command, args)


def test_arg_router_NEW_raise_req_arg_missing_err():
    command = InputType.NEW
    args = []
    with pytest.raises(RequiredArgMissing) as e:
        arg_router(command, args)
