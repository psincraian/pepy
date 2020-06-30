from datetime import datetime, timedelta, date

from pepy.domain.model import ProjectName, Project, Downloads, ProjectVersionDownloads


def test_project_name_strip_spaces():
    project = ProjectName(" some-project  ")
    assert "some-project" == project.name


def test_set_lowercase_to_project_name():
    project = ProjectName("Some-Project")
    assert "some-project" == project.name

def test_normalize_project_name():
    project = ProjectName("test.project")
    assert "test-project" == project.name

def test_add_project():
    project = Project(ProjectName("random"), Downloads(0))
    assert project.last_downloads() == []


def test_add_downloads_to_project():
    project = Project(ProjectName("random"), Downloads(0))
    date = datetime.now().date()
    version = "2.3.1"
    day_downloads = Downloads(10)
    project.add_downloads(date, version, day_downloads)
    assert project.total_downloads == day_downloads
    assert project.last_downloads() == [ProjectVersionDownloads(date, version, day_downloads)]
    assert project.versions() == {version}


def test_project_replace_downloads():
    project = Project(ProjectName("random"), Downloads(10))
    date = datetime.now().date()
    version = "2.3.1"
    day_downloads = Downloads(5)
    project.add_downloads(date, version, day_downloads + Downloads(20))
    project.add_downloads(date, version, day_downloads)
    assert project.total_downloads == Downloads(15)
    assert project.last_downloads() == [ProjectVersionDownloads(date, version, day_downloads)]
    assert project.versions() == {version}


def test_remove_old_data():
    project = Project(ProjectName("random"), Downloads(10))
    old_date = datetime.now().date() - timedelta(days=181)
    limit_date = datetime.now().date() - timedelta(days=180)
    now_date = datetime.now().date()
    project.add_downloads(old_date, "2.3.1", Downloads(10))
    project.add_downloads(limit_date, "2.3.0", Downloads(20))
    project.add_downloads(now_date, "2.3.2", Downloads(30))
    assert project.total_downloads == Downloads(70)
    assert project.last_downloads() == [
        ProjectVersionDownloads(limit_date, "2.3.0", Downloads(20)),
        ProjectVersionDownloads(now_date, "2.3.2", Downloads(30)),
    ]
    assert {"2.3.0", "2.3.2"}.issubset(project.versions())


def test_update_min_date_when_no_other_downloads():
    project = Project(ProjectName("random"), Downloads(10))
    project.add_downloads(date(2019, 3, 9), "0.0.6", Downloads(20))
    project.add_downloads(date(2020, 4, 10), "0.0.2", Downloads(10))
    project.add_downloads(date(2020, 4, 10), "0.0.4", Downloads(10))
    assert project.total_downloads == Downloads(50)
    assert project.last_downloads() == [
        ProjectVersionDownloads(date(2020, 4, 10), "0.0.2", Downloads(10)),
        ProjectVersionDownloads(date(2020, 4, 10), "0.0.4", Downloads(10)),
    ]
    assert project.versions() == {"0.0.6", "0.0.2", "0.0.4"}
    assert project.min_date == date(2020, 4, 10)

def test_filter_date():
    project = Project(ProjectName("random"), Downloads(10))
    project.add_downloads(date(2020, 3, 9), "0.0.6", Downloads(20))
    project.add_downloads(date(2020, 4, 10), "0.0.2", Downloads(10))
    project.add_downloads(date(2020, 4, 10), "0.0.4", Downloads(10))
    project.add_downloads(date(2020, 4, 11), "0.0.4", Downloads(10))
    assert project.total_downloads == Downloads(60)
    assert project.last_downloads(date(2020, 4, 10)) == [
        ProjectVersionDownloads(date(2020, 4, 10), "0.0.2", Downloads(10)),
        ProjectVersionDownloads(date(2020, 4, 10), "0.0.4", Downloads(10)),
        ProjectVersionDownloads(date(2020, 4, 11), "0.0.4", Downloads(10)),
    ]
    assert project.versions() == {"0.0.6", "0.0.2", "0.0.4"}
    assert project.min_date == date(2020, 3, 9)
