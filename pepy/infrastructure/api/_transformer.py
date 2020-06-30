from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict

from natsort import natsorted

from pepy.domain.model import Project


def transform_project(project: Project) -> Dict:
    day_downloads = defaultdict(int)
    month_ago = datetime.now().date() - timedelta(days=30)
    last_downloads = project.last_downloads(month_ago)
    last_downloads.reverse()
    for d in last_downloads:
        day_downloads[d.date.isoformat()] += d.downloads.value
    downloads = {date: downloads for date, downloads in day_downloads.items()}

    return {
        "id": project.name.name,
        "total_downloads": project.total_downloads.value,
        "downloads": downloads,
    }


def transform_project_v2(project: Project) -> Dict:
    day_downloads = defaultdict(lambda: defaultdict(int))
    month_ago = datetime.now().date() - timedelta(days=30)
    last_downloads = project.last_downloads(month_ago)
    for d in last_downloads:
        day_downloads[d.date.isoformat()][d.version] = d.downloads.value

    return {
        "id": project.name.name,
        "total_downloads": project.total_downloads.value,
        "versions": natsorted(list(project.versions())),
        "downloads": day_downloads,
    }
