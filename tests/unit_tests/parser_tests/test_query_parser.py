import pytest

from timer_logic.arg_parsers.query_parse import QueryCommandArgParser
from utils.command_enums import InputType
from utils.exceptions import InvalidArgument


@pytest.fixture
def basic_params():
    params = [
        'd=30',
        'p=123',
        '+chron',
    ]
    return params


def test_time_param(basic_params):
    command = InputType.QUERY
    q = QueryCommandArgParser(command, basic_params)
    result = q.parse()
    assert isinstance(result, tuple)
    assert result[1]['query_time_period'] == '30'


def test_project_param(basic_params):
    command = InputType.QUERY
    q = QueryCommandArgParser(command, basic_params)
    result = q.parse()
    assert result[1]['query_projects'] == '123'


def test_chron_param(basic_params):
    command = InputType.QUERY
    q = QueryCommandArgParser(command, basic_params)
    result = q.parse()
    assert result[1]['chron'] is True


@pytest.fixture
def empty_params():
    empty = [
        'd=',
        'p='
    ]
    return empty


def test_empty_params(empty_params):
    command = InputType.QUERY
    q = QueryCommandArgParser(command, empty_params)
    result = q.parse()
    assert result[1]['query_time_period'] == '0'
    assert result[1]['query_projects'] == '0'


def test_no_params():
    command = InputType.QUERY
    q = QueryCommandArgParser(command, [])
    result = q.parse()
    assert result[1]['query_time_period'] == '0'
    assert result[1]['query_projects'] == '0'
    assert result[1]['query_level'] == 2


def test_query_level_p():
    command = InputType.QUERY
    q = QueryCommandArgParser(command, ['+p'])
    result = q.parse()
    assert result[1]['query_level'] == 0


def test_query_level_s():
    command = InputType.QUERY
    q = QueryCommandArgParser(command, ['+s'])
    result = q.parse()
    assert result[1]['query_level'] == 1


def test_query_level_l():
    command = InputType.QUERY
    q = QueryCommandArgParser(command, ['+l'])
    result = q.parse()
    assert result[1]['query_level'] == 2


@pytest.fixture
def multiple_levels_all():
    return ['+p', '+s', '+l']


def test_query_level_hierarchy_all(multiple_levels_all):
    command = InputType.QUERY
    q = QueryCommandArgParser(command, multiple_levels_all)
    result = q.parse()
    assert result[1]['query_level'] == 2


def test_query_level_hierarchy_all_sorted(multiple_levels_all):
    command = InputType.QUERY
    multiple_levels_all.sort()
    q = QueryCommandArgParser(command, multiple_levels_all)
    result = q.parse()
    assert result[1]['query_level'] == 2


def test_query_level_hierarchy_ps(multiple_levels_all):
    command = InputType.QUERY
    levels = [x for x in multiple_levels_all if x != '+l']
    q = QueryCommandArgParser(command, levels)
    result = q.parse()
    assert result[1]['query_level'] == 1


def test_query_level_hierarchy_sp(multiple_levels_all):
    command = InputType.QUERY
    levels = [x for x in multiple_levels_all if x != '+l']
    levels.sort(reverse=True)
    q = QueryCommandArgParser(command, levels)
    result = q.parse()
    assert result[1]['query_level'] == 1


def test_query_level_hierarchy_sl(multiple_levels_all):
    command = InputType.QUERY
    levels = [x for x in multiple_levels_all if x != '+p']
    levels.sort(reverse=True)
    q = QueryCommandArgParser(command, levels)
    result = q.parse()
    assert result[1]['query_level'] == 2


def test_query_level_hierarchy_ls(multiple_levels_all):
    command = InputType.QUERY
    levels = [x for x in multiple_levels_all if x != '+p']
    levels.sort()
    q = QueryCommandArgParser(command, levels)
    result = q.parse()
    assert result[1]['query_level'] == 2


def test_query_level_hierarchy_pl(multiple_levels_all):
    command = InputType.QUERY
    levels = [x for x in multiple_levels_all if x != '+s']
    levels.sort(reverse=True)
    q = QueryCommandArgParser(command, levels)
    result = q.parse()
    assert result[1]['query_level'] == 2


def test_query_level_hierarchy_lp(multiple_levels_all):
    command = InputType.QUERY
    levels = [x for x in multiple_levels_all if x != '+s']
    levels.sort()
    q = QueryCommandArgParser(command, levels)
    result = q.parse()
    assert result[1]['query_level'] == 2


@pytest.fixture
def additional_args():
    return ['p=123', 'd=30', '+s', 'fart']


def test_parser_ignores_additional_args(additional_args):
    command = InputType.QUERY
    q = QueryCommandArgParser(command, additional_args)
    result = q.parse()
    assert len(result[1]) == 3


def test_parser_raises_invalid_arg_exception():
    command = InputType.QUERY
    with pytest.raises(InvalidArgument):
        q = QueryCommandArgParser(command, ['blah='])
        q.parse()
