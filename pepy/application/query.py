import math
from typing import List

import requests

from pepy.domain.exception import ProjectNotFoundException
from pepy.domain.model import ProjectName, Badge, Project, ProjectDownloads, Downloads
from pepy.domain.repository import ProjectRepository


class DownloadsNumberFormatter:
    _MILLNAMES = ['', 'k', 'M', 'G', 'T']

    def format(self, downloads: Downloads) -> str:
        digits = int(math.floor(0 if downloads.value == 0 else math.log10(abs(downloads.value)) / 3))
        millidx = max(0, min(len(self._MILLNAMES) - 1, digits))
        value = math.floor(downloads.value / 10 ** (3 * millidx))
        if millidx == 0:
            return '{}{}'.format(value, self._MILLNAMES[millidx])
        return '{}{}'.format(value, self._MILLNAMES[millidx])


class BadgeProvider:
    _MILLNAMES = ['', 'k', 'M', 'G', 'T']

    def __init__(self, project_repository: ProjectRepository, downloads_formatter: DownloadsNumberFormatter):
        self._project_repository = project_repository
        self._downloads_formatter = downloads_formatter

    def generate_badge(self, project_name: ProjectName) -> Badge:
        project = self._project_repository.find(project_name)
        if project is None:
            raise ProjectNotFoundException(project_name)
        downloads = self._downloads_formatter.format(project.downloads)
        r = requests.get('https://img.shields.io/badge/downloads-{}-blue.svg'.format(downloads))
        return Badge(project_name, r.content.decode('utf-8'))


class ProjectProvider:
    def __init__(self, project_repository: ProjectRepository):
        self._project_repository = project_repository

    def find(self, project_name: ProjectName) -> Project:
        project = self._project_repository.find(project_name)
        if project is None:
            raise ProjectNotFoundException(project_name)
        return project

    def for_home(self) -> List[Project]:
        return self._project_repository.find_random_projects(10)

    def last_downloads(self, project_name: ProjectName) -> List[ProjectDownloads]:
        return self._project_repository.last_downloads(project_name)
