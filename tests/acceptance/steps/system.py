from datetime import datetime

from behave import given, then
from behave.runner import Context
from freezegun import freeze_time

from pepy.domain.model import ProjectName, ProjectDownloads, Downloads
from tests.tools.stub import ProjectStub


@given("today is {date}")
def step_impl(context: Context, date: str):
    freezer = freeze_time(date)
    freezer.start()