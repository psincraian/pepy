import math
from typing import List

import requests

from pepy.domain.exception import ProjectNotFoundException
from pepy.domain.model import ProjectName, Badge, Project
from pepy.domain.repository import ProjectRepository


class BadgeProvider:
    _MILLNAMES = ['', ' Thousand', ' Million', ' Billion', ' Trillion']

    def __init__(self, project_repository: ProjectRepository):
        self._project_repository = project_repository

    def generate_badge(self, project_name: ProjectName) -> Badge:
        project = self._project_repository.find(project_name)
        if project is None:
            raise ProjectNotFoundException(project_name)
        downloads = self._format_downloads(project.downloads.value)
        r = requests.get('https://img.shields.io/badge/downloads-{}-blue.svg'.format(downloads))
        return Badge(project_name, r.content.decode('utf-8'))

    def _format_downloads(self, n: int) -> str:
        digits = int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))
        millidx = max(0, min(len(self._MILLNAMES) - 1, digits))
        if millidx == 0:
            return '{:.0f}{}'.format(n / 10 ** (3 * millidx), self._MILLNAMES[millidx])
        return '{:.2f}{}'.format(n / 10 ** (3 * millidx), self._MILLNAMES[millidx])


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
