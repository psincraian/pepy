from abc import ABC, abstractmethod
from typing import Optional

from pepy.domain.read_model import ProjectProjection


class ProjectView(ABC):
    @abstractmethod
    def find(self, project_name: str) -> Optional[ProjectProjection]:
        pass
