import sys
from collections import namedtuple
from datetime import datetime

from utils.exceptions import HandlerNotFound
from utils.command_enums import InputType
from utils.const import LOG_COMMANDS, QUERY_COMMANDS, STATUS_CHECK
from utils.time_string_converter import TimeStringToDateTimeObj
from timer_logic.command_mediator import run_mediator


LogArgs = namedtuple("LogArgs", "time name")


def intake(args):

    if len(args) > 4:
        print('Too many arguments. Please try again.')
    elif len(args) == 1:
        print('Argument needed.')  # Create a help?
    else:
        try:
            run_mediator(arg_parser(args[1:]))
        except HandlerNotFound as error:
            print(error)


def arg_parser(args: list) -> dict:

    try:
        command = InputType[args[0].upper()]
        command_args = arg_named_tuple(command, args[1:])
        return {'command': command, 'command_args': command_args}
    except KeyError:
        raise InvalidArgument(f"{args[0]} is not a command")


def arg_named_tuple(command, command_args):
    if command in LOG_COMMANDS:
        if len(command_args) == 1 and command == InputType.START:
            time = datetime.now()
            return LogArgs(name=command_args[0], time=time)
        elif len(command_args) == 1 and command != InputType.START:
            time = TimeStringToDateTimeObj(command_args[0]).get_datetime_obj()
            return LogArgs(time=time, name=None)
        if len(command_args) == 2:
            time = TimeStringToDateTimeObj(command_args[0]).get_datetime_obj()
            return LogArgs(time=time, name=command_args[2])
    elif command in QUERY_COMMANDS:
        pass
    elif command in STATUS_CHECK:
        pass


if __name__ == '__main__':
    intake(sys.argv)
