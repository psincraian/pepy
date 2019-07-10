import traceback
from flask import Flask, request, Response

from pepy.infrastructure import container
from pepy.infrastructure.api import api

app = Flask(__name__)
app.config.from_object(container.config)
app.register_blueprint(api, url_prefix='/api')


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


@app.errorhandler(Exception)
def handle_exception(error: Exception):
    container.logger.critical(f"Error: {error} Traceback: \n {traceback.format_exc()}")
    return "<h1>Internal server error :'(</h1>"
