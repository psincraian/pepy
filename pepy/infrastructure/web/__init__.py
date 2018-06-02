from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, flash, send_from_directory, send_file, Response

from pepy.application.command import UpdateDownloads
from pepy.domain.exception import DomainException
from pepy.domain.model import ProjectName, Password
from pepy.infrastructure import container
from pepy.infrastructure.web._form import SearchForm

app = Flask(__name__)
app.config.from_object(container.config)


@app.route('/', methods=["GET", "POST"])
def index_action():
    form = SearchForm()
    if form.validate_on_submit():
        project_name = form.project_name.data
        return redirect('/count/%s' % project_name)
    projects = container.project_provider.for_home()
    return render_template('index.html', form=form, projects=projects)


@app.route('/count/<project_name>')
def count_action(project_name):
    project_name = ProjectName(project_name)
    project = container.project_provider.find(project_name)
    badge = container.badge_query.generate_badge(project_name)
    return render_template('count.html', project=project, badge=badge)


@app.route('/project/<project_name>')
def project_action(project_name):
    project_name = ProjectName(project_name)
    project = container.project_provider.find(project_name)
    badge = container.badge_query.generate_badge(project_name)
    downloads = container.project_provider.last_downloads(project_name)
    return render_template('project.html', project=project, badge=badge, downloads=downloads)


@app.route('/badge/<project_name>')
def badge_action(project_name):
    badge = container.badge_query.generate_badge(ProjectName(project_name))
    return Response(badge.image, mimetype='image/svg+xml', headers={'Cache-Control': 'max-age=86400'})


@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/task/update_downloads', methods=["POST"])
def update_downloads():
    date = datetime.now() - timedelta(days=1)
    password = request.args.get('password', '')
    container.command_bus.publish(UpdateDownloads(date.date(), Password(password)))
    return "Updated :-)"


@app.errorhandler(DomainException)
def handle_domain_exception(error: DomainException):
    flash(error.message(), 'danger')
    url = request.referrer if request.referrer is not None else '/'
    return redirect(url)
