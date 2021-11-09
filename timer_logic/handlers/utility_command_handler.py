from typing import Union

from .command_handler_base_class import Handler
from timer_database.dbManager import DbUpdate, DbQuery
from command_classes.commands import *

from config.config_manager import ConfigFetch
from config.config_manager import ConfigUpdater
from timer_session.timer_session import Session
from timer_session.timer_session import write_session_data_to_json
from timer_session.timer_session import fetch_helper_func
from utils.command_enums import InputType


class UtilityCommandHandler(Handler):

    def __init__(self, command: UtilityCommand, session: Session):
        self.session = session
        self.command = command

    def handle(self):
        if self.command.get_command_type() == InputType.FETCH:
            self._fetch_project()
        elif self.command.get_command_type() == InputType.STATUS:
            self._status_check()
        elif self.command.get_command_type() == InputType.NEW:
            self._new_project()

    def _fetch_project(self):
        project_id = (self.command.get_project_id(),)  # This works even though PyCharm disagrees
        results = DbQuery().fetch_project(project_id)
        project_name = results[1]
        fetch_helper_func(self.session, project_name, self.command.get_project_id())
        write_session_data_to_json(self.session)
        print(f'Fetched {self.session.project_name} -- Now in queue')

    def _new_project(self):
        tup = (self.command.get_project_name(), 1)
        project = DbUpdate().create_project(tup)
        print(f'{self.command.get_project_name()} [ID: {project}] created!!!')

    def _status_check(self):
        # Todo: This will need to be reworked later
        if self.session.project_name and self.session.last_command != InputType.NO_SESSION:
            print(f'Current project: {self.session.project_name}')
            print(f'Session started on {self.session.session_start_time}')
            print(f'Last command {self.session.last_command.name.upper()} on {self.session.last_command_time}')
        elif self.session.project_name:
            print(f'Project Queued Up: {self.session.project_name}')
            print(f'No session in progress')
        else:
            print('No project queued and no session in progress.')
