import os
from behave.runner import Context


def before_all(context: Context):
    os.environ["APPLICATION_ENV"] = "test"
    from pepy.infrastructure import container
    from pepy.infrastructure.web import app
    context.container = container
    context.client = app.test_client()


def before_scenario(context, _):
    with context.container.db_connection, context.container.db_connection.cursor() as cursor:
        cursor.execute("TRUNCATE projects CASCADE")
