import logging
from typing import Optional, List

from psycopg2.extensions import connection
from psycopg2.extras import execute_values, execute_batch

from pepy.domain.model import Project, ProjectName, ProjectDownloads, Downloads
from pepy.domain.repository import ProjectRepository


class DBProjectRepository(ProjectRepository):
    def __init__(self, conn: connection):
        self._conn = conn

    def find(self, project_name: ProjectName) -> Optional[Project]:
        with self._conn, self._conn.cursor() as cursor:
            cursor.execute("SELECT name, downloads FROM projects WHERE name = %s", (project_name.name,))
            data = cursor.fetchall()
            if len(data) == 0:
                return None
            return Project(ProjectName(data[0][0]), Downloads(data[0][1]))

    def find_random_projects(self, nr_items: int = 10) -> List[Project]:
        with self._conn, self._conn.cursor() as cursor:
            cursor.execute("SELECT name, downloads FROM projects ORDER BY random() LIMIT %s;", (nr_items,))
            data = cursor.fetchall()
            return [Project(ProjectName(row[0]), Downloads(row[1])) for row in data]

    def save_projects(self, projects: List[Project]):
        with self._conn, self._conn.cursor() as cursor:
            values = [(p.name.name, p.downloads.value) for p in projects]
            execute_values(cursor, "INSERT INTO projects(name, downloads) VALUES %s", values)

    def update_downloads(self, projects_downloads: List[ProjectDownloads]):
        with self._conn, self._conn.cursor() as cursor:
            values = [{'downloads':  pd.downloads.value, 'project': pd.name.name} for pd in projects_downloads]
            sql = "UPDATE projects SET downloads = downloads + %(downloads)s WHERE name = %(project)s"
            execute_batch(cursor, sql, values)

    def save_day_downloads(self, project_downloads: List[ProjectDownloads]):
        with self._conn, self._conn.cursor() as cursor:
            values = [(pd.name.name, pd.day, pd.downloads.value) for pd in project_downloads]
            sql = "INSERT INTO downloads_per_day(name, date, downloads) VALUES (%s, %s, %s)"
            execute_batch(cursor, sql, values)
