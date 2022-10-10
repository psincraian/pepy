import json
import re
from behave import *
from behave.runner import Context


@when("I send the {method} request to {url}")
def step_impl(context: Context, method: str, url: str):
    if method == "GET":
        context.response = context.client.get(url)
    else:
        raise ValueError("Method " + method + " is not valid")


@then("the response status code should be {code:d}")
def step_impl(context: Context, code: int):
    assert int(code) == context.response.status_code, "Result status code is {}".format(context.response.status_code)


@step("the response should contain")
def step_impl(context: Context):
    raw_result = context.response.data.decode()
    result = re.sub(r"\s+", "", raw_result)
    expect = re.sub(r"\s+", "", context.text)
    assert expect in result, "Result is {}".format(raw_result)


@step("the api response should be")
def step_impl(context):
    raw_result = context.response.data.decode()
    result = re.sub(r"\s+", "", raw_result)
    expect = re.sub(r"\s+", "", context.text)
    assert json.loads(expect) == json.loads(result), "Result is {}".format(raw_result)
