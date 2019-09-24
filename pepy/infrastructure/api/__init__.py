import json

from flask import Blueprint
from pepy.infrastructure import container
from pepy.infrastructure.api._transformer import transform_project, transform_project_item

api = Blueprint("api", __name__)


@api.route("/projects/<project_name>", methods=["GET"])
def project_action(project_name):
    project = container.project_provider.find(project_name)
    return json.dumps(transform_project(project))


@api.route("/projects", methods=["GET"])
def project_find():
    projects = container.project_provider.for_home()
    return json.dumps([transform_project_item(p) for p in projects])
