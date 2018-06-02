from datetime import datetime

from behave import given
from behave.runner import Context

from pepy.domain.model import ProjectName, ProjectDownloads, Downloads
from tests.tools.stub import ProjectStub


@given("the following projects exists")
def step_impl(context: Context):
    projects = [ProjectStub.from_plain_data(**row.as_dict()) for row in context.table]
    context.container.project_repository.save_projects(projects)


@given("the {name} project with the following downloads")
def step_impl(context: Context, name: str):
    project_name = ProjectName(name)
    project = ProjectStub.create(project_name)
    context.container.project_repository.save_projects([project])
    downloads = []
    for row in context.table:
        date = datetime.strptime(row['date'], '%Y-%m-%d').date()
        downloads.append(ProjectDownloads(project_name, Downloads(row['downloads']), date))
    context.container.project_repository.save_day_downloads(downloads)
