import pytest

from pepy.infrastructure import container
from pepy.infrastructure.db_repository import DBProjectRepository
from tests.tools.stub import ProjectStub, ProjectDownloadsStub


@pytest.fixture()
def project_repository():
    conn = container.db_connection
    with conn.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE projects CASCADE")
    yield DBProjectRepository(conn)


def test_update_downloads(project_repository: DBProjectRepository):
    project = ProjectStub.create()
    project_repository.save_projects([project])
    project_downloads = ProjectDownloadsStub.create(name=project.name)
    project_repository.update_downloads([project_downloads])
    result = find_project(project.name.name)
    assert project_downloads.downloads.value + project.downloads.value == result["downloads"]


def find_project(project_name: str):
    with container.db_connection, container.db_connection.cursor() as cursor:
        cursor.execute("SELECT name, downloads FROM projects where name = %s", (project_name, ))
        data = cursor.fetchall()
        return {"name":  data[0][0], "downloads":  data[0][1]}
