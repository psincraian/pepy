from collections import defaultdict
from typing import Dict

from pepy.domain.model import Project


def transform_project(project: Project) -> Dict:
    day_downloads = defaultdict(int)
    for d in project.last_downloads():
        day_downloads[d.date.isoformat()] += d.downloads.value
    downloads = {date: downloads for date, downloads in day_downloads.items()}

    return {
        "id": project.name.name,
        "total_downloads": project.total_downloads.value,
        "downloads": downloads,
    }


def transform_project_v2(project: Project) -> Dict:
    day_downloads = defaultdict(lambda: defaultdict(int))
    for d in project.last_downloads():
        day_downloads[d.date.isoformat()][d.version] = d.downloads.value

    return {
        "id": project.name.name,
        "total_downloads": project.total_downloads.value,
        "versions": sorted(list(project.versions())),
        "downloads": day_downloads,
    }
