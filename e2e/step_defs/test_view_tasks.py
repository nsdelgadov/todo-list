from pytest_bdd import given, parsers, scenarios, then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from tasks.models import Task

scenarios("../features/view_tasks.feature")


# ----- Given (preconditions) -----


@given(parsers.parse('a task titled "{title}" exists and is not done'))
def _given_pending_task(title):
    Task.objects.create(title=title, done=False)


@given(parsers.parse('a task titled "{title}" exists and is done'))
def _given_done_task(title):
    Task.objects.create(title=title, done=True)


@given("there are no tasks")
def _given_no_tasks():
    Task.objects.all().delete()


# ----- When (actions) -----


@when("I open the app")
def _when_open_app(browser, live_server):
    browser.get(live_server.url + "/")


# ----- Then (expectations) -----


def _wait_until_main_contains(browser, expected):
    WebDriverWait(browser, 10).until(
        lambda b: expected in b.find_element(By.TAG_NAME, "main").text
    )


@then(parsers.parse('I see "{title}" displayed as not done'))
def _then_pending(browser, title):
    _wait_until_main_contains(browser, f"[ ] {title}")


@then(parsers.parse('I see "{title}" displayed as done'))
def _then_done(browser, title):
    _wait_until_main_contains(browser, f"[x] {title}")


@then(parsers.parse('I see "{message}"'))
def _then_message(browser, message):
    _wait_until_main_contains(browser, message)
