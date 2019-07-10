import traceback
from datetime import datetime, timedelta
from flask import Flask, request, send_from_directory, Response

from pepy.application.command import UpdateDownloads
from pepy.domain.model import ProjectName, Password
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


@app.route("/robots.txt")
def robots():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route("/task/update_downloads", methods=["POST"])
def update_downloads():
    raw_date = request.args.get("date")
    try:
        if raw_date is not None:
            date = datetime.strptime(raw_date, "%Y-%m-%d")
        else:
            date = datetime.now() - timedelta(days=1)
    except ValueError:
        return Response("Date format should be YYYY-mm-dd", 400)

    password = request.args.get("password", "")
    container.command_bus.publish(UpdateDownloads(date.date(), Password(password)))
    return "Updated :-)"


@app.errorhandler(Exception)
def handle_exception(error: Exception):
    container.logger.critical(f"Error: {error} Traceback: \n {traceback.format_exc()}")
    return "<h1>Internal server error :'(</h1>"
