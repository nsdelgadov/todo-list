from pytest_bdd import parsers, scenarios, then, when
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


@when(parsers.parse("I shorten the new task input to {length:d} characters"))
def _shorten_new_task_input(browser, length):
    field = browser.find_element(
        By.CSS_SELECTOR, "input[aria-label='New task title']"
    )
    field.clear()
    field.send_keys("a" * length)


@then(parsers.parse("the new task input contains {length:d} characters"))
def _new_task_input_has_length(browser, length):
    field = browser.find_element(
        By.CSS_SELECTOR, "input[aria-label='New task title']"
    )
    WebDriverWait(browser, 10).until(
        lambda _: len(field.get_attribute("value")) == length
    )


@then(parsers.parse('I do not see "{message}"'))
def _do_not_see_message(browser, message):
    WebDriverWait(browser, 10).until(
        lambda b: message not in b.find_element(By.TAG_NAME, "main").text
    )


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
