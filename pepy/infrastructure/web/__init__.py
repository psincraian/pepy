import json
import traceback

from flask import Flask, Response, request
from werkzeug.exceptions import HTTPException

from pepy.domain.exception import DomainException, ProjectNotFoundException
from pepy.infrastructure import container
from pepy.infrastructure.api import api

app = Flask(__name__)
app.config.from_object(container.config)
app.register_blueprint(api, url_prefix="/api")


@app.route("/health-check")
def health_check_action():
    return json.dumps({"status": "healthy"})


@app.route("/badge/<project_name>")
def badge_action(project_name):
    badge = container.badge_service.generate_badge(project_name)
    return Response(badge.image, mimetype="image/svg+xml", headers={"Cache-Control": "max-age=86400"})


@app.route("/badge/<project_name>/month")
def badge_month_action(project_name):
    badge = container.badge_service.generate_last_30_days_badge(project_name)
    return Response(badge.image, mimetype="image/svg+xml", headers={"Cache-Control": "max-age=86400"})


@app.route("/badge/<project_name>/week")
def badge_week_action(project_name):
    badge = container.badge_service.generate_last_7_days_badge(project_name)
    return Response(badge.image, mimetype="image/svg+xml", headers={"Cache-Control": "max-age=86400"})


@app.route("/personalized-badge/<project_name>")
def personalized_badge_action(project_name):
    badge = container.personalized_badge_service.generate(
        project_name,
        request.args.get("period", "total"),
        request.args.get("left_color", "green"),
        request.args.get("right_color", "green"),
        request.args.get("left_text", "downloads/month"),
        request.args.get("units", "international_system"),
    )
    return Response(badge.image, mimetype="image/svg+xml")


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


@app.errorhandler(HTTPException)
def handle_http_exception(error: HTTPException):
    return Response(json.dumps({"error": error.code, "message": error.description}), status=error.code)


@app.errorhandler(Exception)
def handle_exception(error: Exception):
    if isinstance(error, DomainException):
        return handle_domain_exception(error)
    container.logger.critical(f"Error: {error} Traceback: \n {traceback.format_exc()}")
    return Response(json.dumps({"error": 500, "message": "Internal server error"}), status=500)
