import datetime
from abc import ABC, abstractmethod
from typing import List, Iterable, Optional

from pepy.domain.model import Project, ProjectDownloads, BQDownloads


class ProjectRepository(ABC):
    @abstractmethod
    def save_projects(self, projects: List[Project]):
        pass

    @abstractmethod
    def update_downloads(self, projects_downloads: List[ProjectDownloads]):
        pass

    @abstractmethod
    def save_day_downloads(self, project_downloads: List[ProjectDownloads]):
        pass

    @abstractmethod
    def get(self, project)-> Optional[Project]:
        pass

    @abstractmethod
    def save(self, project: Project):
        pass


class DownloadsExtractor(ABC):
    @abstractmethod
    def get_downloads(self, date: datetime.date) -> List[ProjectDownloads]:
        pass

    @abstractmethod
    def get_version_downloads(self, date: datetime.date) -> Iterable[BQDownloads]:
        pass