import pytest
from timer_session.time_log_stack import TimeLogStack


@pytest.fixture
def times():
    return [
            ['10/05/21_15:12:37', '10/05/21_17:12:19'],
            ['10/06/21_09:12:28', '10/06/21_09:33:20'],
            ['10/07/21_11:12:18', '10/07/21_15:34:00'],
            ['10/10/21_07:12:13', '10/10/21_08:44:51']
            ]


def test_stack_with_times(times):
    stack = TimeLogStack(times)
    assert len(stack.get_stack_data()) == 4
