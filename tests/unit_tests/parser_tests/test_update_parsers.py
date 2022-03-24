import datetime

import pytest

from src.timer_logic.arg_parsers.update_parse import UpdateCommandArgParser
from src.utils.command_enums import InputType

from src.utils.exceptions import InvalidArgument


def test_rename_parse():
    command = InputType.RENAME
    params = ['p=2', 'This is a new name']
    q = UpdateCommandArgParser(command, params).parse()
    result = q
    assert result[1]['project_id'] == 2
    assert result[1]['new_name'] == 'This is a new name'


def test_rename_parse_project_id_not_int():
    command = InputType.RENAME
    params = ['p=2a', 'This is a new name']
    with pytest.raises(InvalidArgument) as e:
        UpdateCommandArgParser(command, params).parse()


def test_rename_parse_not_enough_args():
    command = InputType.RENAME
    params = ['p=2']
    with pytest.raises(InvalidArgument) as e:
        UpdateCommandArgParser(command, params).parse()


def test_rename_parse_too_many_args():
    command = InputType.RENAME
    params = ['p=2', 'This is a new name', 'gooba goba']
    with pytest.raises(InvalidArgument) as e:
        UpdateCommandArgParser(command, params).parse()