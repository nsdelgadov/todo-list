import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def browser():
    """Headless Chrome instance fresh per test.

    Selenium 4 ships Selenium Manager, which downloads the matching
    chromedriver automatically — contributors only need Chrome itself.
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
