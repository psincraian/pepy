import json
from datetime import timedelta, datetime

from flask import Blueprint, request, abort, jsonify

from pepy.domain.exception import ProjectNotFoundException
from pepy.domain.model import Password
from pepy.infrastructure import container
from pepy.infrastructure.api._transformer import transform_project, transform_project_v2, transform_v1_admin_project

api = Blueprint("api", __name__)


@api.route("/projects/<project_name>", methods=["GET"])
def project_action(project_name):
    from_date = datetime.now().date() - timedelta(days=30)
    project = container.project_repository.get(project_name, downloads_from=from_date)
    if project is None:
        raise ProjectNotFoundException(project_name)
    response = jsonify(transform_project(project))
    add_cache_control(response)
    return response


def add_cache_control(response):
    response.headers.add("Cache-Control", "public, max-age=3600, stale-if-error=3600, stale-while-revalidate=60")


@api.route("/v2/projects/<project_name>", methods=["GET"])
def get_project_action_v2(project_name):
    from_date = datetime.now().date() - timedelta(days=90)
    project = container.project_repository.get(project_name, downloads_from=from_date)
    if project is None:
        raise ProjectNotFoundException(project_name)

    response = jsonify(transform_project_v2(project))
    add_cache_control(response)
    return response


@api.route("/v1/admin/projects/<project_name>", methods=["GET"])
def get_admin_project(project_name):
    project = container.project_repository.get(project_name)
    if project is None:
        raise ProjectNotFoundException(project_name)
    password = request.args.get("password")
    if password is None or not container.admin_password_checker.check(Password(password)):
        abort(401)
    return jsonify(transform_v1_admin_project(project))
