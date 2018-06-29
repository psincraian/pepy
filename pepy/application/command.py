import csv
import datetime
from logging import Logger
from typing import TextIO

from commandbus import Command, CommandHandler

from pepy.application.helper import AdminPasswordChecker
from pepy.domain.exception import InvalidAdminPassword
from pepy.domain.model import Project, Password, Downloads, ProjectName
from pepy.domain.repository import ProjectRepository, DownloadsExtractor


class ImportDownloadsFile(Command):
    def __init__(self, file: TextIO):
        self.file = file


class ImportDownloadsFileHandler(CommandHandler):
    def __init__(self, project_repository: ProjectRepository):
        self._project_repository = project_repository

    def handle(self, cmd: ImportDownloadsFile):
        reader = csv.reader(cmd.file, delimiter=",")
        next(reader)
        projects = [Project(ProjectName(r[0]), Downloads(r[1])) for r in reader]
        self._project_repository.save_projects(projects)


class UpdateDownloads(Command):
    def __init__(self, date: datetime.date, password: Password):
        self.password = password
        self.date = date


class UpdateDownloadsHandler(CommandHandler):
    def __init__(
        self,
        project_repository: ProjectRepository,
        downloads_extractor: DownloadsExtractor,
        admin_password_checker: AdminPasswordChecker,
        logger: Logger,
    ):
        self._project_repository = project_repository
        self._downloads_extractor = downloads_extractor
        self._admin_password_checker = admin_password_checker
        self._logger = logger

    def handle(self, cmd: UpdateDownloads):
        if not self._admin_password_checker.check(cmd.password):
            self._logger.info("Invalid password")
            raise InvalidAdminPassword(cmd.password)
        self._logger.info(f"Getting downloads from date {cmd.date}...")
        pd = self._downloads_extractor.get_downloads(cmd.date)
        self._logger.info(f"Retrieved {len(pd)} downloads. Saving to db...")
        # Add new projects if they don't exist before
        self._project_repository.save_projects([Project(p.name, Downloads(0)) for p in pd])
        self._logger.info("New projects saved")
        self._project_repository.save_day_downloads(pd)
        self._logger.info("Downloads saved")
        self._project_repository.update_downloads(pd)
        self._logger.info("Total downloads updated")
