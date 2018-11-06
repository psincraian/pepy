import datetime
from abc import ABC, abstractmethod
from typing import List

from pepy.domain.model import Project, ProjectDownloads


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


class DownloadsExtractor(ABC):
    @abstractmethod
    def get_downloads(self, date: datetime.date) -> List[ProjectDownloads]:
        pass
