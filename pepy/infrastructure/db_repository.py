from typing import List

from psycopg2.extensions import connection
from psycopg2.extras import execute_batch

from pepy.domain.model import Project, ProjectDownloads
from pepy.domain.repository import ProjectRepository


class DBProjectRepository(ProjectRepository):
    def __init__(self, conn: connection):
        self._conn = conn

    def save_projects(self, projects: List[Project]):
        with self._conn, self._conn.cursor() as cursor:
            values = [(p.name.name, p.downloads.value) for p in projects]
            execute_batch(
                cursor, "INSERT INTO projects(name, downloads) VALUES (%s, %s) ON CONFLICT DO NOTHING", values
            )

    def update_downloads(self, projects_downloads: List[ProjectDownloads]):
        with self._conn, self._conn.cursor() as cursor:
            values = [{"downloads": pd.downloads.value, "project": pd.name.name} for pd in projects_downloads]
            sql = "UPDATE projects SET downloads = downloads + %(downloads)s WHERE name = %(project)s"
            execute_batch(cursor, sql, values)

    def save_day_downloads(self, project_downloads: List[ProjectDownloads]):
        with self._conn, self._conn.cursor() as cursor:
            values = [(pd.name.name, pd.day, pd.downloads.value) for pd in project_downloads]
            sql = "INSERT INTO downloads_per_day(name, date, downloads) VALUES (%s, %s, %s)"
            execute_batch(cursor, sql, values)
