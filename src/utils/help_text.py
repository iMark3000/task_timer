from .command_enums import InputType

"""
Help texts for different features. Currently only set up for the QUERY command.
"""


class Help:

    def __init__(self, command: InputType, args: list):
        self._command = command
        self._args = args

    def _remove_help_arg(self):
        self._args = [a for a in self._args if a.strip() != '-help' or '-h']

    def _fetch_help(self):
        # ToDo: Plan out a way to store help texts
        print(f'{self._command.name}')
