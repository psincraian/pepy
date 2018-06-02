import csv
import datetime
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
        reader = csv.reader(cmd.file, delimiter=',')
        next(reader)
        projects = [Project(ProjectName(r[0]), Downloads(r[1])) for r in reader]
        self._project_repository.save_projects(projects)


class UpdateDownloads(Command):
    def __init__(self, date: datetime.date, password: Password):
        self.password = password
        self.date = date


class UpdateDownloadsHandler(CommandHandler):
    def __init__(self, project_repository: ProjectRepository, downloads_extractor: DownloadsExtractor,
                 admin_password_checker: AdminPasswordChecker):
        self._project_repository = project_repository
        self._downloads_extractor = downloads_extractor
        self._admin_password_checker = admin_password_checker

    def handle(self, cmd: UpdateDownloads):
        if not self._admin_password_checker.check(cmd.password):
            raise InvalidAdminPassword(cmd.password)
        pd = self._downloads_extractor.get_downloads(cmd.date)
        self._project_repository.save_day_downloads(pd)
        self._project_repository.update_downloads(pd)
