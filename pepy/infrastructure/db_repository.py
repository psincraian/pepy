import datetime
from collections import defaultdict
from typing import List, Optional

from pymongo import ReplaceOne, DESCENDING
from pymongo.database import Database

from pepy.domain.model import Project, ProjectDownloads, ProjectName, Downloads, ProjectVersionDownloads, DayDownloads
from pepy.domain.repository import ProjectRepository


class MongoProjectRepository(ProjectRepository):
    def __init__(self, client: Database):
        self._client = client
        self._client.projects.create_index([("name", DESCENDING)])
        self._client.project_downloads.create_index([("name", DESCENDING)])

    def get(self, project_name: str, downloads_from: datetime.date = None) -> Optional[Project]:
        normalized_name = ProjectName(project_name).name
        project_data = self._client.projects.find_one({"name": normalized_name})
        if project_data is None:
            return None
        project = Project(ProjectName(project_data["name"]), Downloads(project_data["total_downloads"]))
        if "downloads" in project_data:
            downloads = sorted(project_data["downloads"].items(), key=lambda x: x[0])
            for iso_date, version_downloads in downloads:
                for r in version_downloads:
                    date = datetime.date.fromisoformat(iso_date)
                    version = r[0]
                    project.add_downloads(date, version, DayDownloads(r[1], 0))
                    project._repository_saved_downloads.add((iso_date, version))
                    # Don't count the downloads twice
                    project.total_downloads -= Downloads(r[1])
        else:
            if downloads_from is None:
                raw_downloads = self._client.project_downloads.find({"project": normalized_name})
            else:
                raw_downloads = self._client.project_downloads.find(
                    {"project": normalized_name, "date": {"$gte": downloads_from.isoformat()}}
                )
            downloads = sorted(raw_downloads, key=lambda x: x["date"])
            for day_downloads in downloads:
                for version_downloads in day_downloads["downloads"]:
                    pip_downlods = version_downloads["pip_downloads"] if "pip_downlods" in version_downloads else 0
                    project.add_downloads(
                        datetime.date.fromisoformat(day_downloads["date"]),
                        version_downloads["version"],
                        DayDownloads(version_downloads["downloads"], pip_downlods),
                    )
                    # Don't count the downloads twice
                    project.total_downloads -= Downloads(version_downloads["downloads"])
        return project

    def save(self, project: Project):
        project_data = self._convert_project_to_raw(project)
        query = {"name": project.name.name}
        self._client.projects.replace_one(query, project_data, upsert=True)
        downloads_requests = []
        for date, value in self._convert_downloads_to_raw(project).items():
            downloads_requests.append(ReplaceOne({"project": project.name.name, "date": date}, value, upsert=True))
        self._client.project_downloads.bulk_write(downloads_requests)

    def _convert_project_to_raw(self, project):
        data = {
            "name": project.name.name,
            "total_downloads": project.total_downloads.value,
            "monthly_downloads": project.month_downloads().value,
        }
        return data

    def _convert_downloads_to_raw(self, project: Project) -> dict:
        downloads_per_day = defaultdict(list)
        for download in project.last_downloads():
            if not (download.date.isoformat(), download.version) in project._repository_saved_downloads:
                downloads_per_day[download.date.isoformat()].append(
                    {
                        "version": download.version,
                        "downloads": download.downloads.value,
                        "pip_downloads": download.pip_downloads.value,
                    }
                )
        result = {}
        for date, downloads in downloads_per_day.items():
            result[date] = {"project": project.name.name, "date": date, "downloads": downloads}
        return result

    def save_projects(self, projects: List[Project]):
        requests = []
        downloads_requests = []
        for project in projects:
            requests.append(ReplaceOne({"name": project.name.name}, self._convert_project_to_raw(project), upsert=True))
            for date, value in self._convert_downloads_to_raw(project).items():
                downloads_requests.append(ReplaceOne({"project": project.name.name, "date": date}, value, upsert=True))
        self._client.projects.bulk_write(requests)
        self._client.project_downloads.bulk_write(downloads_requests)
