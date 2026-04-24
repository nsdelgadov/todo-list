import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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
