import os

from behave.runner import Context


def before_all(context: Context):
    os.environ["APPLICATION_ENV"] = "test"
    from pepy.infrastructure import container
    from pepy.infrastructure.web import app

    context.container = container
    context.client = app.test_client()


def before_scenario(context, _):
    context.container.mongo_client.pepy_test.projects.remove()
    context.container.mongo_client.pepy_test.project_downloads.remove()
