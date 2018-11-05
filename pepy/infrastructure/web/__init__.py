import traceback
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, flash, send_from_directory, send_file, Response, url_for

from pepy.application.command import UpdateDownloads
from pepy.domain.exception import DomainException
from pepy.domain.model import ProjectName, Password
from pepy.infrastructure import container
from pepy.infrastructure.web._form import SearchForm

app = Flask(__name__)
app.config.from_object(container.config)


@app.route("/", methods=["GET", "POST"])
def index_action():
    form = SearchForm()
    if form.validate_on_submit():
        project_name = form.project_name.data
        return redirect(url_for("project_action", project_name=project_name))
    projects = container.project_provider.for_home()
    return render_template("index.html", form=form, projects=projects)


@app.route("/count/<project_name>")
def count_action(project_name):
    return redirect(url_for("project_action", project_name=project_name), 301)


@app.route("/project/<project_name>")
def project_action(project_name):
    project = container.project_provider.find(project_name)
    return render_template("project.html", project=project, downloads=project.last_downloads)


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


@app.errorhandler(DomainException)
def handle_domain_exception(error: DomainException):
    flash(error.message(), "danger")
    url = request.referrer if request.referrer is not None else "/"
    return redirect(url)


@app.errorhandler(Exception)
def handle_exception(error: Exception):
    container.logger.critical(f"Error: {error} Traceback: \n {traceback.format_exc()}")
    return "<h1>Internal server error :'(</h1>"
