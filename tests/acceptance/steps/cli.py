from behave import *
from behave.runner import Context

from pepy.application.command import ImportTotalDownloads


@when("I run the import_total_downloads with file {file_name}")
def step_impl(context: Context, file_name: str):
    context.container.command_bus.publish(ImportTotalDownloads(file_name))
