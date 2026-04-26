import pytest
from pytest_bdd import given, parsers, then, when
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from tasks.models import Task


# ===== Fixtures =====


@pytest.fixture(autouse=True)
def _live_server(live_server):
    """Ensure pytest-django's live_server (and its transactional_db) is up
    for every e2e scenario.

    pytest-bdd 7.x does not auto-propagate fixtures requested as step
    parameters to the generated test, so without autouse the Given steps
    would fail with 'Database access not allowed' before the When step
    even gets a chance to start the live server.
    """
    return live_server


@pytest.fixture(autouse=True)
def browser():
    """Headless Chrome instance fresh per test.

    Selenium 4 ships Selenium Manager, which downloads the matching
    chromedriver automatically — contributors only need Chrome itself.
    Marked autouse so step functions can request 'browser' as a parameter
    without each test having to list it explicitly.
    """
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,800")
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(20)
    try:
        yield driver
    finally:
        driver.quit()


# ===== Shared step definitions =====
# Steps live here (instead of in step_defs/test_*.py) so any .feature in
# this suite can reuse them. pytest-bdd auto-discovers steps from any
# conftest.py in scope.


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


def _checkbox_for(browser, title):
    # The checkbox is wrapped in a <label> alongside the task title, so the
    # label's normalized text is exactly the title.
    return browser.find_element(
        By.XPATH,
        f"//label[normalize-space()='{title}']/input[@type='checkbox']",
    )


@then(parsers.parse('I see "{title}" displayed as not done'))
def _then_pending(browser, title):
    WebDriverWait(browser, 10).until(
        lambda b: _checkbox_for(b, title).is_selected() is False
    )


@then(parsers.parse('I see "{title}" displayed as done'))
def _then_done(browser, title):
    WebDriverWait(browser, 10).until(
        lambda b: _checkbox_for(b, title).is_selected() is True
    )


@then(parsers.parse('I see "{message}"'))
def _then_message(browser, message):
    _wait_until_main_contains(browser, message)
