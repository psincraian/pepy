import math
from datetime import datetime, timedelta

import requests

from pepy.domain.exception import ProjectNotFoundException
from pepy.domain.model import Badge, Project, Downloads
from pepy.domain.repository import ProjectRepository


class DownloadsNumberFormatter:
    _METRIC_PREFIX = ["", "k", "M", "G", "T", "P"]

    def format(self, downloads: Downloads) -> str:
        if downloads.value == 0:
            return "0"
        digits = int(math.log10(abs(downloads.value)) if downloads else 0)
        millidx = max(0, min(len(self._METRIC_PREFIX) - 1, digits // 3))
        rounded_value = downloads.value // (10 ** (3 * millidx))
        return "{}{}".format(rounded_value, self._METRIC_PREFIX[millidx])


class BadgeService:
    def __init__(self, project_repository: ProjectRepository, downloads_formatter: DownloadsNumberFormatter):
        self._project_repository = project_repository
        self._downloads_formatter = downloads_formatter

    def generate_badge(self, project_name: str) -> Badge:
        project = self._project_repository.get(project_name)
        if project is None:
            raise ProjectNotFoundException(project_name)
        downloads = self._downloads_formatter.format(project.total_downloads)
        r = requests.get("https://img.shields.io/badge/downloads-{}-blue.svg".format(downloads))
        return Badge(project_name, r.content.decode("utf-8"))

    def generate_last_30_days_badge(self, project_name: str) -> Badge:
        project = self._project_repository.get(project_name)
        if project is None:
            raise ProjectNotFoundException(project_name)
        downloads = self._downloads_formatter.format(self._last_downloads(project, 30))
        r = requests.get("https://img.shields.io/badge/downloads/month-{}-blue.svg".format(downloads))
        return Badge(project_name, r.content.decode("utf-8"))

    def generate_last_7_days_badge(self, project_name: str) -> Badge:
        project = self._project_repository.get(project_name)
        if project is None:
            raise ProjectNotFoundException(project_name)
        downloads = self._downloads_formatter.format(self._last_downloads(project, 7))
        r = requests.get("https://img.shields.io/badge/downloads/week-{}-blue.svg".format(downloads))
        return Badge(project_name, r.content.decode("utf-8"))

    @staticmethod
    def _last_downloads(project: Project, days: int) -> Downloads:
        min_date = datetime.now().date() - timedelta(days=days)
        total_downloads = 0
        for d in project.last_downloads():
            if d.date >= min_date:
                total_downloads += d.downloads.value
        return Downloads(total_downloads)
