from behave import given
from behave.runner import Context


@given("the a file named {file_name} with the following content")
def step_impl(context: Context, file_name: str):
    with open(file_name, "w") as f:
        f.write(context.text)
