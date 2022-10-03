import datetime
import random
import uuid

from behave import given, when
from behave.runner import Context

from pepy.application.command import UpdateVersionDownloads
from pepy.domain.model import Password
from pepy.domain.pypi import Row


@given("the following pypi download stats")
def step_impl(context: Context):
    bq_rows = []
    for row in context.table:
        pip_downloads = int(row["pip_downloads"]) if "pip_downloads" in row else int(row["downloads"])
        bq_rows.append(
            Row(
                row["project"],
                row["version"],
                datetime.date.fromisoformat(row["date"]),
                int(row["downloads"]),
                pip_downloads,
            )
        )
    context.container.stats_viewer.set_data(bq_rows)


@given("the {number} projects and pepy")
def step_impl(context: Context, number: str):
    bq_rows = []
    for _ in range(int(number)):
        project = str(uuid.uuid4())
        for d in range(30):
            bq_rows.append(
                Row(
                    project,
                    str(uuid.uuid1()),
                    datetime.datetime.now().date() + datetime.timedelta(days=d),
                    random.randint(1, 100_000_000),
                )
            )
    bq_rows.append(Row("pepy", str(uuid.uuid1()), datetime.datetime.now().date(), random.randint(1, 100_000_000)))
    context.container.stats_viewer.set_data(bq_rows)


@when("I run the update_version_downloads command for date {date_str}")
def step_impl(context: Context, date_str: str):
    date = datetime.date.fromisoformat(date_str)
    context.container.command_bus.publish(UpdateVersionDownloads(date, Password("pepyrocks")))
