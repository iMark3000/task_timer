import sys

from utils.command_enums import InputType
from timer_logic.arg_parse import arg_router
from timer_logic.command_mediator import run_mediator

from utils.exceptions import RequiredArgMissing
from utils.exceptions import InvalidArgument
from utils.exceptions import TooManyCommandArgs
from utils.exceptions import HandlerNotFound


def intake(args):
    try:
        command = InputType[args[1].upper()]
        command_args = args[2:]
        command_dict = arg_router(command, command_args)
        run_mediator(command_dict)
    except KeyError (f"{args[0]} is not a command"):
        pass
    except (RequiredArgMissing, InvalidArgument, TooManyCommandArgs) as e:
        print(e)
    except (HandlerNotFound, InvalidArgument) as error:
        print(error)


if __name__ == '__main__':
    intake(sys.argv)
