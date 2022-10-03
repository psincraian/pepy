from datetime import datetime

from behave import given, then
from behave.runner import Context

from pepy.domain.model import ProjectName, ProjectDownloads, Downloads, DayDownloads
from tests.tools.stub import ProjectStub


@given("the following projects exists")
def step_impl(context: Context):
    projects = [ProjectStub.from_plain_data(**row.as_dict()) for row in context.table]
    context.container.project_repository.save_projects(projects)


@given("the {name} project with the following downloads")
def step_impl(context: Context, name: str):
    project = ProjectStub.create(ProjectName(name), Downloads(0))
    for row in context.table:
        date = datetime.strptime(row["date"], "%Y-%m-%d").date()
        project.add_downloads(date, row["version"], DayDownloads(int(row["downloads"]), int(row["downloads"])))
    context.container.project_repository.save(project)


@given("the following downloads per day exists")
def step_impl(context: Context):
    downloads = []
    for row in context.table:
        date = datetime.strptime(row["date"], "%Y-%m-%d").date()
        downloads.append(ProjectDownloads(ProjectName(row["name"]), Downloads(row["downloads"]), date))
    context.container.project_repository.save_day_downloads(downloads)


@then("the following projects should exist")
def step_impl(context: Context):
    for row in context.table:
        project = context.container.project_repository.get(row["project"])
        assert project is not None
        if "total_downloads" in row:
            assert project.total_downloads == row["total_downloads"]
