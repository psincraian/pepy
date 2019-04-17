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
    downloads = []
    total_downloads = 0
    for row in context.table:
        date = datetime.strptime(row["date"], "%Y-%m-%d").date()
        total_downloads += int(row["downloads"])
        downloads.append(ProjectDownloads(project_name, Downloads(row["downloads"]), date))
    project = ProjectStub.create(project_name, Downloads(total_downloads))
    context.container.project_repository.save_projects([project])
    context.container.project_repository.save_day_downloads(downloads)


@given("the following downloads per day exists")
def step_impl(context: Context):
    downloads = []
    for row in context.table:
        date = datetime.strptime(row["date"], "%Y-%m-%d").date()
        downloads.append(ProjectDownloads(ProjectName(row["name"]), Downloads(row["downloads"]), date))
    context.container.project_repository.save_day_downloads(downloads)
