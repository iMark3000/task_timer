from typing import Union

from src.command_classes.commands_base_class import CommandBaseClass
from src.utils.command_enums import InputType


class ConfigCommand(CommandBaseClass):

    def __init__(self, command: InputType, **kwargs):
        self._view = None
        self._config_toggle = None
        super().__init__(command, **kwargs)

    def is_view(self):
        return self._view

    def toggle(self) -> Union[str, None]:
        return self._config_toggle