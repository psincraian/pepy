from behave import given
from behave.runner import Context

from tests.tools.stub import ProjectStub


@given("the following projects exists")
def step_impl(context: Context):
    projects = [ProjectStub.from_plain_data(**row.as_dict()) for row in context.table]
    context.container.project_repository.save_projects(projects)
