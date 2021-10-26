from utils.command_enums import InputType

#  TODO LOG is not included below
LOG_COMMANDS = [InputType.NEW, InputType.START, InputType.PAUSE, InputType.RESUME, InputType.STOP]

QUERY_COMMANDS = [InputType.PROJECTS, InputType.REPORT]

STATUS_MISC = [InputType.STATUS, InputType.FETCH]

# For validating time entries in timer_logic.arg_parse.py; Includes 'a' in case of 'am'
VALID_TIME_CHARACTERS = '1 2 3 4 5 6 7 8 9 0 p . m : a'.split()

# Alpa chars for name
VALID_NAME_CHARACTERS = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.split()