import pytest

from pepy.domain.model import ProjectName
from pepy.domain.read_model import ProjectProjection
from pepy.infrastructure import container
from pepy.infrastructure.db_repository import DBProjectRepository
from pepy.infrastructure.db_view import DBProjectView
from tests.tools.stub import ProjectStub


@pytest.fixture()
def project_repository():
    conn = container.db_connection
    with conn.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE projects CASCADE")
    yield DBProjectRepository(conn)


@pytest.fixture()
def project_view():
    conn = container.db_orator
    yield DBProjectView(conn)


def test_find_project(project_repository: DBProjectRepository, project_view: DBProjectView):
    project = ProjectStub.create(name=ProjectName("pepy"))
    project_repository.save_projects([project])

    result = project_view.find("pepy")
    expected = ProjectProjection("pepy", project.downloads.value, [])
    assert result == expected


def test_find_project_ignoring_case(project_repository: DBProjectRepository, project_view: DBProjectView):
    project = ProjectStub.create(name=ProjectName("pepy"))
    project_repository.save_projects([project])

    result = project_view.find("PEpy")
    expected = ProjectProjection("pepy", project.downloads.value, [])
    assert result == expected


def test_find_project_ignoring_white_spaces(project_repository: DBProjectRepository, project_view: DBProjectView):
    project = ProjectStub.create(name=ProjectName("pepy"))
    project_repository.save_projects([project])

    result = project_view.find("    pepy  ")
    expected = ProjectProjection("pepy", project.downloads.value, [])
    assert result == expected


def test_find_project_replacing_dots_with_dashes(project_repository: DBProjectRepository, project_view: DBProjectView):
    project = ProjectStub.create(name=ProjectName("pepy-rocks"))
    project_repository.save_projects([project])

    result = project_view.find("pepy.rocks")
    expected = ProjectProjection("pepy-rocks", project.downloads.value, [])
    assert result == expected
