import json
import traceback

from flask import Flask, Response, request, jsonify

from pepy.domain.exception import DomainException, ProjectNotFoundException
from pepy.infrastructure import container
from pepy.infrastructure.api import api

app = Flask(__name__)
app.config.from_object(container.config)
app.register_blueprint(api, url_prefix="/api")


@app.route("/health-check")
def health_check_action():
    return jsonify({"status": "healthy"})


@app.route("/badge/<project_name>")
def badge_action(project_name):
    badge = container.badge_query.generate_badge(project_name)
    return Response(badge.image, mimetype="image/svg+xml", headers={"Cache-Control": "max-age=86400"})


@app.route("/badge/<project_name>/month")
def badge_month_action(project_name):
    badge = container.badge_query.generate_last_30_days_badge(project_name)
    return Response(badge.image, mimetype="image/svg+xml", headers={"Cache-Control": "max-age=86400"})


@app.route("/badge/<project_name>/week")
def badge_week_action(project_name):
    badge = container.badge_query.generate_last_7_days_badge(project_name)
    return Response(badge.image, mimetype="image/svg+xml", headers={"Cache-Control": "max-age=86400"})


def handle_domain_exception(error: DomainException):
    code = None
    message = None
    if isinstance(error, ProjectNotFoundException):
        code = 404
        message = json.dumps({"error": code, "message": error.message()})
    else:
        code = 400
        message = json.dumps({"error": code, "message": error.message()})
    return Response(message, status=code)


@app.errorhandler(Exception)
def handle_exception(error: Exception):
    if isinstance(error, DomainException):
        return handle_domain_exception(error)
    container.logger.critical(f"Error: {error} Traceback: \n {traceback.format_exc()}")
    return Response(json.dumps({"error": 500, "message": "Internal server error"}), status=500)