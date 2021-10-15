from .commands import *
from .handlers import LogCommandHandler
from utils.const import LOG_COMMANDS


def command_creator(command: dict):  # TODO: Request? Command? What is it?
    # TODO: Add commands as you create them
    command_directory = {
        InputType.START: StartCommand,
        InputType.PAUSE: PauseCommand,
        InputType.RESUME: ResumeCommand,
        InputType.STOP: StopCommand
    }

    command_type = command['command']

    if command_type == InputType.START:
        if len(command['command_args']) == 2:
            name, time = command['command_args'][:]
            command_obj = StartCommand(command_type, name, time=time)
        else:
            name = command['command_args'][0]
            command_obj = StartCommand(command_type, name)
    else:
        if command['command_args']:
            time = command['command_args'][0]
            command_obj = command_directory.get(command_type)(command_type, time=time)
        else:
            command_obj = command_directory.get(command_type)(command_type)

    return command_obj


def router(command:Command):
    if command.get_command_type() in LOG_COMMANDS:
        LogCommandHandler(command)

def run():
