from abc import ABC, abstractmethod
from typing import Optional, List

from pepy.domain.read_model import ProjectProjection, ProjectListProjection


class ProjectView(ABC):
    @abstractmethod
    def find(self, project_name: str) -> Optional[ProjectProjection]:
        pass

    @abstractmethod
    def find_random_projects(self, number_of_projects) -> List[ProjectListProjection]:
        pass
