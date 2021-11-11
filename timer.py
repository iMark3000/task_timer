#!/usr/bin/env python

import sys

from utils.command_enums import InputType
from timer_logic.arg_parsers.arg_parser_router import arg_router
from timer_logic.command_mediator import run_mediator

from utils.exceptions import RequiredArgMissing
from utils.exceptions import InvalidArgument
from utils.exceptions import TooManyCommandArgs
from utils.exceptions import HandlerNotFound
from config.config_manager import ConfigFetch


def intake(args):
    try:
        command = InputType[args[1].upper()]
        command_args = args[2:]
        pass_to_mediator(arg_router(command, command_args))
    except KeyError:
        print(f"{args[1]} is not a command")


def pass_to_mediator(command_dict):
    try:
        run_mediator(command_dict)
    except (RequiredArgMissing, InvalidArgument, TooManyCommandArgs) as e:
        print(e)
    except (HandlerNotFound, InvalidArgument) as error:
        print(error)


if __name__ == '__main__':
    if ConfigFetch().fetch_test_status():
        print('***USING TEST DB***')
    intake(sys.argv)
