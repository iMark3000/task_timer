from string import ascii_lowercase

from utils.command_enums import InputType

#  TODO LOG is not included below
LOG_COMMANDS = [InputType.START, InputType.PAUSE, InputType.RESUME, InputType.STOP]

QUERY_COMMANDS = [InputType.PROJECTS, InputType.REPORT, InputType.PROJECTS]

UTILITY_COMMANDS = [InputType.NEW, InputType.STATUS, InputType.FETCH]

# For validating time entries in timer_logic.arg_parse.py; Includes 'a' in case of 'am'
VALID_TIME_CHARACTERS = '1 2 3 4 5 6 7 8 9 0 p P . m M : a A'.split()

# Alpha chars for name
VALID_NAME_CHARACTERS = [char for char in ascii_lowercase]