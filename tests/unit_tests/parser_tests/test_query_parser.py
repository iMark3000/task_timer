import datetime

import pytest

from src.timer_logic.arg_parsers.query_parse import QueryCommandArgParser
from src.utils.command_enums import InputType


@pytest.fixture
def basic_params():
    params = [
        'd=30',
        'p=123',
    ]
    return params


def test_time_param(basic_params):
    command = InputType.QUERY
    q = QueryCommandArgParser(command, basic_params)
    result = q.parse()
    assert result[1]['query_time_period'] == 30


def test_time_param_w():
    command = InputType.QUERY
    q = QueryCommandArgParser(command, ['d=w'])
    result = q.parse()
    assert result[1]['query_time_period'] == 'w'


def test_time_param_m():
    command = InputType.QUERY
    q = QueryCommandArgParser(command, ['d=m'])
    result = q.parse()
    assert result[1]['query_time_period'] == 'm'


def test_time_param_y():
    command = InputType.QUERY
    q = QueryCommandArgParser(command, ['d=y'])
    result = q.parse()
    assert result[1]['query_time_period'] == 'y'


def test_time_param_cy():
    command = InputType.QUERY
    q = QueryCommandArgParser(command, ['d=CY'])
    result = q.parse()
    assert result[1]['query_time_period'] == 'CY'


def test_time_param_at():
    command = InputType.QUERY
    q = QueryCommandArgParser(command, ['d=at'])
    result = q.parse()
    assert result[1]['query_time_period'] == 'at'


def test_project_param(basic_params):
    command = InputType.QUERY
    q = QueryCommandArgParser(command, basic_params)
    result = q.parse()
    assert result[1]['query_projects'] == (123,)


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
    assert result[1]['query_time_period'] == 0
    assert result[1]['query_projects'] == (0,)


def test_no_params():
    command = InputType.QUERY
    q = QueryCommandArgParser(command, [])
    result = q.parse()
    assert result[1]['query_time_period'] == 'W'
    assert result[1]['query_projects'] == (0,)
    assert result[1]['query_level'] == 1


def test_query_level_p():
    command = InputType.QUERY
    q = QueryCommandArgParser(command, ['+p'])
    result = q.parse()
    assert result[1]['query_level'] == 3


def test_query_level_s():
    command = InputType.QUERY
    q = QueryCommandArgParser(command, ['+s'])
    result = q.parse()
    assert result[1]['query_level'] == 2


def test_query_level_l():
    command = InputType.QUERY
    q = QueryCommandArgParser(command, ['+l'])
    result = q.parse()
    assert result[1]['query_level'] == 1


@pytest.fixture
def multiple_levels_all():
    return ['+p', '+s', '+l']


def test_query_level_hierarchy_all(multiple_levels_all):
    command = InputType.QUERY
    q = QueryCommandArgParser(command, multiple_levels_all)
    result = q.parse()
    assert result[1]['query_level'] == 1


def test_query_level_hierarchy_all_sorted(multiple_levels_all):
    command = InputType.QUERY
    multiple_levels_all.sort()
    q = QueryCommandArgParser(command, multiple_levels_all)
    result = q.parse()
    assert result[1]['query_level'] == 1


def test_query_level_hierarchy_ps(multiple_levels_all):
    command = InputType.QUERY
    levels = [x for x in multiple_levels_all if x != '+l']
    q = QueryCommandArgParser(command, levels)
    result = q.parse()
    assert result[1]['query_level'] == 2


def test_query_level_hierarchy_sp(multiple_levels_all):
    command = InputType.QUERY
    levels = [x for x in multiple_levels_all if x != '+l']
    levels.sort(reverse=True)
    q = QueryCommandArgParser(command, levels)
    result = q.parse()
    assert result[1]['query_level'] == 2


def test_query_level_hierarchy_sl(multiple_levels_all):
    command = InputType.QUERY
    levels = [x for x in multiple_levels_all if x != '+p']
    levels.sort(reverse=True)
    q = QueryCommandArgParser(command, levels)
    result = q.parse()
    assert result[1]['query_level'] == 1


def test_query_level_hierarchy_ls(multiple_levels_all):
    command = InputType.QUERY
    levels = [x for x in multiple_levels_all if x != '+p']
    levels.sort()
    q = QueryCommandArgParser(command, levels)
    result = q.parse()
    assert result[1]['query_level'] == 1


def test_query_level_hierarchy_pl(multiple_levels_all):
    command = InputType.QUERY
    levels = [x for x in multiple_levels_all if x != '+s']
    levels.sort(reverse=True)
    q = QueryCommandArgParser(command, levels)
    result = q.parse()
    assert result[1]['query_level'] == 1


def test_query_level_hierarchy_lp(multiple_levels_all):
    command = InputType.QUERY
    levels = [x for x in multiple_levels_all if x != '+s']
    levels.sort()
    q = QueryCommandArgParser(command, levels)
    result = q.parse()
    assert result[1]['query_level'] == 1


@pytest.fixture
def additional_args():
    return ['p=123', 'd=30', '+s', '+p', 'nutmeg', 'r=3']


def test_parser_ignores_additional_args(additional_args):
    command = InputType.QUERY
    q = QueryCommandArgParser(command, additional_args)
    result = q.parse()
    print(result)
    assert len(result[1]) == 3


@pytest.fixture
def basic_args_WO_dates():
    return ['p=123', '+l']


def test_start_date_only(basic_args_WO_dates):
    basic_args_WO_dates.append('s=11/2/2021')
    command = InputType.QUERY
    q = QueryCommandArgParser(command, basic_args_WO_dates)
    result = q.parse()
    assert 'start_date' in result[1].keys()
    assert result[1]['start_date'] == datetime.date(year=2021, month=11, day=2)
    assert 'end_date' not in result[1].keys()


def test_end_date_only(basic_args_WO_dates):
    basic_args_WO_dates.append('e=11/2/2021')
    command = InputType.QUERY
    q = QueryCommandArgParser(command, basic_args_WO_dates)
    result = q.parse()
    assert 'end_date' in result[1].keys()
    assert result[1]['end_date'] == datetime.date(year=2021, month=11, day=2)
    assert 'start_date' not in result[1].keys()


def test_start_and_end_date(basic_args_WO_dates):
    basic_args_WO_dates.append('e=11/2/2021')
    basic_args_WO_dates.append('s=10/15/2021')
    command = InputType.QUERY
    q = QueryCommandArgParser(command, basic_args_WO_dates)
    result = q.parse()
    print(f'\n{result}')
    assert 'start_date' in result[1].keys()
    assert result[1]['start_date'] == datetime.date(year=2021, month=10, day=15)
    assert 'end_date' in result[1].keys()
    assert result[1]['end_date'] == datetime.date(year=2021, month=11, day=2)
