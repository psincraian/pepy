from typing import Dict

from pepy.domain.read_model import ProjectProjection, ProjectListProjection


def transform_project(project: ProjectProjection) -> Dict:
    return {
        "id": project.name,
        "total_downloads": project.total_downloads,
        "downloads": {d.date.isoformat(): d.downloads for d in project.last_downloads},
    }


def transform_project_item(project: ProjectListProjection) -> Dict:
    return {"id": project.name, "total_downloads": project.total_downloads}
