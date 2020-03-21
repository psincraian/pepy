import datetime
from typing import Optional, List

from pymongo import MongoClient

from pepy.domain.read_model import ProjectProjection, DownloadProjection, ProjectListProjection
from pepy.domain.view import ProjectView


class MongoProjectView(ProjectView):
    def __init__(self, client: MongoClient):
        self._client = client.test

    def find(self, project_name: str) -> Optional[ProjectProjection]:
        project_data = self._client.projects.find_one({"name": project_name})
        if project_data is None:
            return None
        downloads = []
        for date, version_downloads in project_data['downloads'].items():
            day_downloads = 0
            for r in version_downloads:
                day_downloads += r[1]
            downloads.append(DownloadProjection(datetime.date.fromisoformat(date), day_downloads))
        project = ProjectProjection(project_data["name"], project_data["total_downloads"], downloads)

        return project

    def find_random_projects(self, number_of_projects) -> List[ProjectListProjection]:
        pass