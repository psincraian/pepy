import json

from flask import Blueprint, request, abort

from pepy.domain.exception import ProjectNotFoundException
from pepy.domain.model import Password
from pepy.infrastructure import container
from pepy.infrastructure.api._transformer import transform_project, transform_project_v2, transform_v1_admin_project

api = Blueprint("api", __name__)


@api.route("/projects/<project_name>", methods=["GET"])
def project_action(project_name):
    project = container.project_repository.get(project_name)
    if project is None:
        raise ProjectNotFoundException(project_name)
    return json.dumps(transform_project(project))


@api.route("/v2/projects/<project_name>", methods=["GET"])
def get_project_action_v2(project_name):
    project = container.project_repository.get(project_name)
    if project is None:
        raise ProjectNotFoundException(project_name)
    return json.dumps(transform_project_v2(project))


@api.route("/v1/admin/projects/<project_name>", methods=["GET"])
def get_admin_project(project_name):
    project = container.project_repository.get(project_name)
    if project is None:
        raise ProjectNotFoundException(project_name)
    password = request.args.get("password")
    if password is None or not container.admin_password_checker.check(Password(password)):
        abort(401)
    return json.dumps(transform_v1_admin_project(project))
