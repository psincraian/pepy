import datetime
from abc import ABC, abstractmethod
from typing import Optional, List

from pepy.domain.model import Project, ProjectName, ProjectDownloads


class ProjectRepository(ABC):
    @abstractmethod
    def find(self, project_name: ProjectName) -> Optional[Project]:
        pass

    @abstractmethod
    def find_random_projects(self, nr_items: int = 10) -> List[Project]:
        pass

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
