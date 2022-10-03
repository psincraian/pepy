import random
from datetime import date, datetime, timedelta
from typing import List

from pepy.domain.model import ProjectName, Downloads, Project, ProjectDownloads


class ProjectNameStub:
    @staticmethod
    def create() -> ProjectName:
        project_names = ["climoji", "pepy", "commandbus", "flask", "behave"]
        return ProjectName(random.choice(project_names))


class DownloadsStub:
    @staticmethod
    def create(min_value: int = 0, max_value: int = 999999) -> Downloads:
        return Downloads(random.randint(min_value, max_value), random.randint(min_value, max_value))


class ProjectStub:
    @staticmethod
    def create(name: ProjectName = None, downloads: Downloads = None) -> Project:
        name = name or ProjectNameStub.create()
        downloads = downloads or DownloadsStub.create()
        return Project(name, downloads)

    @staticmethod
    def from_plain_data(name: str = None, downloads: int = None) -> Project:
        name = ProjectName(name) if name is not None else ProjectNameStub.create()
        downloads = Downloads(downloads, downloads) if downloads is not None else DownloadsStub.create()
        return ProjectStub.create(name=name, downloads=downloads)


class ProjectDownloadsStub:
    @staticmethod
    def create(name: ProjectName = None, downloads: Downloads = None, day: date = None) -> ProjectDownloads:
        name = name or ProjectNameStub.create()
        downloads = downloads or DownloadsStub.create()
        day = day or datetime.now().date()
        return ProjectDownloads(name, downloads, day)

    @staticmethod
    def create_consecutive(name: ProjectName = None, first_day: date = None, days: int = 10) -> List[ProjectDownloads]:
        name = name or ProjectNameStub.create()
        first_day = first_day or datetime.now().date()
        return [ProjectDownloadsStub.create(name=name, day=first_day - timedelta(days=i)) for i in range(days)]
