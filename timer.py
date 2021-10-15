import sys

from utils.exceptions import InvalidArgument
from utils.command_enums import InputType
from handlers.command_router import command_creator


def intake(args):

    if len(args) > 4:
        print('Too many arguments. Please try again.')
    elif len(args) == 1:
        print('Argument needed.')  # Create a help?
    else:
        try:
            command_creator(arg_parser(args[1:]))
        except InvalidArgument as error:
            print(error)


def arg_parser(args: list) -> dict:

    try:
        command = InputType[args[0].upper()]
        command_args = args[1:]
        return {'command': command, 'command_args': command_args}
    except KeyError:
        raise InvalidArgument(f"{args[0]} is not a command")


if __name__ == '__main__':
    intake(sys.argv)
