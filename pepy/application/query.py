import math
from typing import List

import requests

from pepy.domain.exception import ProjectNotFoundException
from pepy.domain.model import ProjectName, Badge, Project, ProjectDownloads, Downloads
from pepy.domain.read_model import ProjectProjection, ProjectListProjection
from pepy.domain.repository import ProjectRepository
from pepy.domain.view import ProjectView


class DownloadsNumberFormatter:
    _METRIC_PREFIX = ["", "k", "M", "G", "T", "P"]

    def format(self, downloads: int) -> str:
        digits = int(math.log10(abs(downloads)) if downloads else 0)
        millidx = max(0, min(len(self._METRIC_PREFIX) - 1, digits // 3))
        rounded_value = downloads // (10 ** (3 * millidx))
        return "{}{}".format(rounded_value, self._METRIC_PREFIX[millidx])


class BadgeProvider:
    def __init__(self, project_view: ProjectView, downloads_formatter: DownloadsNumberFormatter):
        self._project_repository = project_view
        self._downloads_formatter = downloads_formatter

    def generate_badge(self, project_name: str) -> Badge:
        project = self._project_repository.find(project_name)
        if project is None:
            raise ProjectNotFoundException(project_name)
        downloads = self._downloads_formatter.format(project.total_downloads)
        r = requests.get("https://img.shields.io/badge/downloads-{}-blue.svg".format(downloads))
        return Badge(project_name, r.content.decode("utf-8"))

    def generate_last_30_days_badge(self, project_name: str) -> Badge:
        project = self._project_repository.find(project_name)
        if project is None:
            raise ProjectNotFoundException(project_name)
        downloads = self._downloads_formatter.format(project.total_downloads_last_30_days)
        r = requests.get("https://img.shields.io/badge/downloads/month-{}-blue.svg".format(downloads))
        return Badge(project_name, r.content.decode("utf-8"))

    def generate_last_7_days_badge(self, project_name: str) -> Badge:
        project = self._project_repository.find(project_name)
        if project is None:
            raise ProjectNotFoundException(project_name)
        downloads = self._downloads_formatter.format(project.total_downloads_last_7_days)
        r = requests.get("https://img.shields.io/badge/downloads/week-{}-blue.svg".format(downloads))
        return Badge(project_name, r.content.decode("utf-8"))


class ProjectProvider:
    def __init__(self, project_repository: ProjectRepository, project_view: ProjectView):
        self._project_repository = project_repository
        self._project_view = project_view

    def find(self, project_name: str) -> ProjectProjection:
        project = self._project_view.find(project_name)
        if project is None:
            raise ProjectNotFoundException(project_name)
        return project

    def for_home(self) -> List[ProjectListProjection]:
        return self._project_view.find_most_download_last_day(10)

    def last_downloads(self, project_name: ProjectName) -> List[ProjectDownloads]:
        return self._project_repository.last_downloads(project_name)
