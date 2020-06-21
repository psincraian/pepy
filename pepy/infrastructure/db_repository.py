import datetime
from typing import List, Optional

from pymongo import ReplaceOne, DESCENDING
from pymongo.database import Database

from pepy.domain.model import Project, ProjectDownloads, ProjectName, Downloads
from pepy.domain.repository import ProjectRepository


class MongoProjectRepository(ProjectRepository):
    def __init__(self, client: Database):
        self._client = client
        self._client.projects.create_index([("name", DESCENDING)])

    def get(self, project_name: str) -> Optional[Project]:
        normalized_name = ProjectName(project_name).name
        project_data = self._client.projects.find_one({"name": normalized_name})
        if project_data is None:
            return None
        project = Project(ProjectName(project_data["name"]), Downloads(project_data["total_downloads"]))
        downloads = sorted(project_data["downloads"].items(), key=lambda x: x[0])
        for date, version_downloads in downloads:
            for r in version_downloads:
                project.add_downloads(datetime.date.fromisoformat(date), r[0], Downloads(r[1]))
                # Don't count the downloads twice
                project.total_downloads -= Downloads(r[1])
        return project

    def save(self, project: Project):
        data = self._convert_to_raw(project)
        query = {"name": project.name.name}
        self._client.projects.replace_one(query, data, upsert=True)

    def _convert_to_raw(self, project):
        data = {
            "name": project.name.name,
            "total_downloads": project.total_downloads.value,
            "downloads": {
                date.isoformat(): [(version, x.value) for version, x in list(versions.items())]
                for date, versions in project._latest_downloads.items()
            },
        }
        return data

    def save_projects(self, projects: List[Project]):
        requests = []
        for project in projects:
            requests.append(ReplaceOne({"name": project.name.name}, self._convert_to_raw(project), upsert=True))
        self._client.projects.bulk_write(requests)

    def update_downloads(self, projects_downloads: List[ProjectDownloads]):
        pass

    def save_day_downloads(self, project_downloads: List[ProjectDownloads]):
        pass
