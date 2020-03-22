import json

from flask import Blueprint

from pepy.domain.exception import ProjectNotFoundException
from pepy.infrastructure import container
from pepy.infrastructure.api._transformer import transform_project

api = Blueprint("api", __name__)


@api.route("/projects/<project_name>", methods=["GET"])
def project_action(project_name):
    project = container.project_repository.get(project_name)
    if project is None:
        raise ProjectNotFoundException(project_name)
    return json.dumps(transform_project(project))