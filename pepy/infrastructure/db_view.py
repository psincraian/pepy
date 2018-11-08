from typing import Optional, List

from orator import DatabaseManager

from pepy.domain.read_model import ProjectProjection, DownloadProjection, ProjectListProjection
from pepy.domain.view import ProjectView


class DBProjectView(ProjectView):
    def __init__(self, db_manager: DatabaseManager):
        self._db = db_manager

    def find(self, project_name: str) -> Optional[ProjectProjection]:
        project_name = project_name.lower()
        data = self._db.table("projects").where("name", project_name).first()

        if data is None:
            return None

        last_downloads_data = (
            self._db.table("downloads_per_day").where("name", project_name).order_by("date", "desc").limit(30).get()
        )

        last_downloads = [DownloadProjection(row["date"], row["downloads"]) for row in last_downloads_data]

        return ProjectProjection(data["name"], data["downloads"], last_downloads)

    def find_random_projects(self, number_of_projects: int) -> List[ProjectListProjection]:
        data = self._db.table("projects") \
            .order_by_raw(f"random()") \
            .limit(number_of_projects) \
            .get()

        # sort the projects in the given order
        return [ProjectListProjection(row["name"], row["downloads"]) for row in data]
