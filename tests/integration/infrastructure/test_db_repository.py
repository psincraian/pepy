import datetime

import pytest

from pepy.domain.model import Downloads, ProjectVersionDownloads, ProjectName
from pepy.domain.repository import ProjectRepository
from pepy.infrastructure import container
from pymongo import MongoClient


@pytest.fixture()
def repository():
    return container.project_repository


@pytest.fixture()
def mongo_client():
    return container.mongo_client


def test_retrieve_project(mongo_client: MongoClient, repository: ProjectRepository):
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
