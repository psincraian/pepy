import datetime
import timeit
from logging import Logger
from typing import Iterable, List, Generator

from commandbus import Command, CommandHandler

from pepy.application.admin_password_checker import AdminPasswordChecker
from pepy.domain.exception import InvalidAdminPassword
from pepy.domain.model import Project, Password, Downloads, ProjectName
from pepy.domain.pypi import StatsViewer, Row
from pepy.domain.repository import ProjectRepository


class UpdateVersionDownloads(Command):
    def __init__(self, date: datetime.date, password: Password):
        self.password = password
        self.date = date


class UpdateVersionDownloadsHandler(CommandHandler):
    def __init__(
            self,
            project_repository: ProjectRepository,
            stats_viewer: StatsViewer,
            admin_password_checker: AdminPasswordChecker,
            logger: Logger,
    ):
        self._project_repository = project_repository
        self._stats_viewer = stats_viewer
        self._admin_password_checker = admin_password_checker
        self._logger = logger

    def handle(self, cmd: UpdateVersionDownloads):
        if not self._admin_password_checker.check(cmd.password):
            self._logger.info("Invalid password")
            raise InvalidAdminPassword(cmd.password)
        self._logger.info(f"Getting downloads from date {cmd.date}...")
        stats_result = self._stats_viewer.get_version_downloads(cmd.date)
        self._logger.info(f"Retrieved {stats_result.total_rows} downloads. Saving to db...")
        start_time = timeit.default_timer()
        for batch in self._batch(stats_result.rows, 1_000):
            projects = {}
            for row in batch:
                project = None
                if row.project in projects:
                    project = projects.get(row.project)
                else:
                    project = self._project_repository.get(row.project)
                if project is None:
                    project = Project(ProjectName(row.project), Downloads(0))
                project.add_downloads(row.date, row.version, Downloads(row.downloads))
                projects[row.project] = project
            self._project_repository.save_projects(list(projects.values()))
        end_time = timeit.default_timer()
        print(f"Total time + {(end_time - start_time):.4f}")
        self._logger.info("Total downloads updated")

    def _batch(self, rows: Iterable[Row], batch_size: int) -> Generator[List[Row], None, None]:
        data = []
        for r in rows:
            data.append(r)
            if len(data) == batch_size:
                yield data
                data = []
        yield data
