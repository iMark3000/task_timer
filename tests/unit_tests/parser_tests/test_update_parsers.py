import datetime

import pytest

from src.timer_logic.arg_parsers.update_parse import UpdateCommandArgParser
from src.utils.command_enums import InputType

from src.utils.exceptions import InvalidArgument
from src.utils.exceptions import RequiredArgMissing


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


def test_rename_parse_missing_project_id_flag():
    command = InputType.RENAME
    params = ['2', 'This is a new name']
    with pytest.raises(RequiredArgMissing) as e:
        UpdateCommandArgParser(command, params).parse()


def test_merge_parse_with_multiple_ids():
    command = InputType.MERGE
    params = ['2', '3', '4', '5']
    q = UpdateCommandArgParser(command, params).parse()
    result = q
    assert result[1]['new_project'] is False
    assert result[1]['merge_to'] == 2
    assert result[1]['absorbed'] == [3, 4, 5]


def test_merge_parse_with_multiple_ids_name_first():
    command = InputType.MERGE
    params = ['name=Hello Beautiful', '2', '3', '4', '5']
    q = UpdateCommandArgParser(command, params).parse()
    result = q
    assert result[1]['new_project'] is True
    assert result[1]['merge_to'] == 'Hello Beautiful'
    assert result[1]['absorbed'] == [2, 3, 4, 5]


def test_merge_parse_with_multiple_ids_name_not_first():
    command = InputType.MERGE
    params = ['2', '3', 'name=Hello Beautiful',  '4', '5']
    q = UpdateCommandArgParser(command, params).parse()
    result = q
    assert result[1]['new_project'] is True
    assert result[1]['merge_to'] == 'Hello Beautiful'
    assert result[1]['absorbed'] == [2, 3, 4, 5]


def test_merge_parse_with_one_id():
    command = InputType.MERGE
    params = ['2']
    with pytest.raises(RequiredArgMissing) as e:
        UpdateCommandArgParser(command, params).parse()


def test_merge_parse_with_one_id_and_name():
    command = InputType.MERGE
    params = ['2', 'name=this will not work']
    with pytest.raises(RequiredArgMissing) as e:
        UpdateCommandArgParser(command, params).parse()
        print(f'\n{e}')


def test_merge_parse_with_non_ints_in_id():
    command = InputType.MERGE
    params = ['2', 'fa']
    with pytest.raises(InvalidArgument) as e:
        UpdateCommandArgParser(command, params).parse()
        print(f'\n{e}')