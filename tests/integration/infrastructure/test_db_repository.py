import datetime

import pytest

from pepy.domain.model import Downloads, ProjectVersionDownloads, ProjectName, Project, DayDownloads
from pepy.domain.repository import ProjectRepository
from pepy.infrastructure import container
from pymongo import MongoClient, InsertOne


@pytest.fixture()
def repository():
    return container.project_repository


@pytest.fixture()
def mongo_client():
    client = container.mongo_client
    client.pepy_test.projects.remove()
    client.pepy_test.project_downloads.remove()

    return client


def test_save_project_with_new_format(mongo_client: MongoClient, repository: ProjectRepository):
    project = Project(ProjectName("climoji"), Downloads(100))
    project.add_downloads(datetime.date(2020, 3, 31), "2.0", DayDownloads(40, 40))
    project.add_downloads(datetime.date(2020, 3, 31), "2.0.1", DayDownloads(30, 30))
    project.add_downloads(datetime.date(2020, 4, 1), "2.0", DayDownloads(20, 20))
    repository.save(project)

    data = mongo_client.pepy_test.projects.find_one({"name": project.name.name})
    expected_data = {"name": "climoji", "total_downloads": 190, "monthly_downloads": 0}
    for key, value in expected_data.items():
        assert key in data
        assert value == data[key]
    downloads_data = sorted(
        mongo_client.pepy_test.project_downloads.find({"project": project.name.name}), key=lambda x: x["date"]
    )
    expected_downloads_data = [
        {
            "project": "climoji",
            "date": "2020-03-31",
            "downloads": [{"version": "2.0", "downloads": 40}, {"version": "2.0.1", "downloads": 30}],
        },
        {"project": "climoji", "date": "2020-04-01", "downloads": [{"version": "2.0", "downloads": 20}]},
    ]
    assert len(expected_downloads_data) == len(downloads_data)
    for i in range(len(expected_downloads_data)):
        for key, value in expected_downloads_data[i].items():
            assert key in downloads_data[i]
            assert value == downloads_data[i][key]


def test_save_many_projects_with_new_format(mongo_client: MongoClient, repository: ProjectRepository):
    project = Project(ProjectName("climoji"), Downloads(100))
    project.add_downloads(datetime.date(2020, 3, 31), "2.0", DayDownloads(40, 10))
    project.add_downloads(datetime.date(2020, 3, 31), "2.0.1", DayDownloads(30, 10))
    project.add_downloads(datetime.date(2020, 4, 1), "2.0", DayDownloads(20, 10))
    repository.save_projects([project])

    data = mongo_client.pepy_test.projects.find_one({"name": project.name.name})
    expected_data = {"name": "climoji", "total_downloads": 190, "monthly_downloads": 0}
    for key, value in expected_data.items():
        assert key in data
        assert value == data[key]
    downloads_data = sorted(
        mongo_client.pepy_test.project_downloads.find({"project": project.name.name}), key=lambda x: x["date"]
    )
    expected_downloads_data = [
        {
            "project": "climoji",
            "date": "2020-03-31",
            "downloads": [{"version": "2.0", "downloads": 40}, {"version": "2.0.1", "downloads": 30}],
        },
        {"project": "climoji", "date": "2020-04-01", "downloads": [{"version": "2.0", "downloads": 20}]},
    ]
    assert len(expected_downloads_data) == len(downloads_data)
    for i in range(len(expected_downloads_data)):
        for key, value in expected_downloads_data[i].items():
            assert key in downloads_data[i]
            assert value == downloads_data[i][key]


def test_do_not_touch_already_saved_data(mongo_client: MongoClient, repository: ProjectRepository):
    # Used for performance reasons
    data = {
        "name": "climoji",
        "total_downloads": 1100,
    }
    query = {"name": "climoji"}
    mongo_client.pepy_test.projects.replace_one(query, data, upsert=True)
    downloads_data = [
        InsertOne({"project": "climoji", "date": "2020-04-01", "downloads": [{"version": "2.0", "downloads": 30}]}),
    ]
    mongo_client.pepy_test.project_downloads.bulk_write(downloads_data)

    project = repository.get("climoji")
    project.add_downloads(datetime.date(2020, 4, 1), "2.0", DayDownloads(1, 1))
    repository.save(project)
    downloads_data = sorted(
        mongo_client.pepy_test.project_downloads.find({"project": project.name.name}), key=lambda x: x["date"]
    )
    expected_downloads_data = [
        {"project": "climoji", "date": "2020-04-01", "downloads": [{"version": "2.0", "downloads": 30}]}
    ]
    assert len(expected_downloads_data) == len(downloads_data)
    for i in range(len(expected_downloads_data)):
        for key, value in expected_downloads_data[i].items():
            assert key in downloads_data[i]
            assert value == downloads_data[i][key]


def test_retrieve_project_with_new_format(mongo_client: MongoClient, repository: ProjectRepository):
    data = {
        "name": "climoji",
        "total_downloads": 1100,
    }
    query = {"name": "climoji"}
    mongo_client.pepy_test.projects.replace_one(query, data, upsert=True)
    downloads_data = [
        InsertOne({"project": "climoji", "date": "2020-04-01", "downloads": [{"version": "2.0", "downloads": 30}]}),
        InsertOne({"project": "climoji", "date": "2020-04-02", "downloads": [{"version": "2.0", "downloads": 10}]}),
        InsertOne({"project": "climoji", "date": "2020-03-31", "downloads": [{"version": "2.0", "downloads": 40}]}),
        InsertOne({"project": "climoji", "date": "2020-04-03", "downloads": [{"version": "2.0", "downloads": 30}]}),
    ]
    mongo_client.pepy_test.project_downloads.bulk_write(downloads_data)

    result = repository.get("climoji")
    assert ProjectName("climoji") == result.name
    assert datetime.date(2020, 3, 31) == result.min_date
    assert Downloads(1100) == result.total_downloads
    expected_last_downloads = [
        ProjectVersionDownloads(datetime.date(2020, 3, 31), "2.0", Downloads(40)),
        ProjectVersionDownloads(datetime.date(2020, 4, 1), "2.0", Downloads(30)),
        ProjectVersionDownloads(datetime.date(2020, 4, 2), "2.0", Downloads(10)),
        ProjectVersionDownloads(datetime.date(2020, 4, 3), "2.0", Downloads(30)),
    ]
    assert expected_last_downloads == result.last_downloads()


def test_retrieve_project_with_old_format(mongo_client: MongoClient, repository: ProjectRepository):
    data = {
        "name": "climoji",
        "total_downloads": 1100,
        "downloads": {
            "2020-04-01": [["2.0", 30]],
            "2020-04-02": [["2.0", 10]],
            "2020-03-31": [["2.0", 40]],
            "2020-04-03": [["2.0", 30]],
        },
    }
    query = {"name": "climoji"}
    mongo_client.pepy_test.projects.replace_one(query, data, upsert=True)

    result = repository.get("climoji")
    assert ProjectName("climoji") == result.name
    assert datetime.date(2020, 3, 31) == result.min_date
    assert Downloads(1100) == result.total_downloads
    expected_last_downloads = [
        ProjectVersionDownloads(datetime.date(2020, 3, 31), "2.0", Downloads(40)),
        ProjectVersionDownloads(datetime.date(2020, 4, 1), "2.0", Downloads(30)),
        ProjectVersionDownloads(datetime.date(2020, 4, 2), "2.0", Downloads(10)),
        ProjectVersionDownloads(datetime.date(2020, 4, 3), "2.0", Downloads(30)),
    ]
    assert expected_last_downloads == result.last_downloads()
