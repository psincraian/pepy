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
