from pytest_bdd import parsers, scenarios, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

scenarios("../features/create_task.feature")


@when(parsers.parse('I type "{text}" in the new task input'))
def _type_in_new_task_input(browser, text):
    field = browser.find_element(
        By.CSS_SELECTOR, "input[aria-label='New task title']"
    )
    field.clear()
    field.send_keys(text)


@when(parsers.parse("I type a title with {length:d} characters in the new task input"))
def _type_title_of_length(browser, length):
    field = browser.find_element(
        By.CSS_SELECTOR, "input[aria-label='New task title']"
    )
    field.clear()
    field.send_keys("a" * length)


@when(parsers.parse('I click "{label}"'))
def _click_button(browser, label):
    # Wait for the button to exist and be enabled. The label is the visible
    # text, which in the form goes from 'Add' → 'Adding…' while the request
    # is in flight, so locating by label avoids flakiness if a previous step
    # left the button mid-submit.
    locator = (By.XPATH, f"//button[normalize-space()='{label}']")
    button = WebDriverWait(browser, 10).until(
        lambda b: b.find_element(*locator) if b.find_element(*locator).is_enabled() else False
    )
    button.click()
