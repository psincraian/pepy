from pepy.domain.model import ProjectName


def test_project_name_strip_spaces():
    project = ProjectName(" some-project  ")
    assert "some-project" == project.name


def test_set_lowercase_to_project_name():
    project = ProjectName("Some-Project")
    assert "some-project" == project.name
