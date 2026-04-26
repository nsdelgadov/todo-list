from pytest_bdd import parsers, scenarios, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

scenarios("../features/edit_task.feature")


@when(parsers.parse('I type "{text}" in the edit input'))
def _type_in_edit_input(browser, text):
    field = WebDriverWait(browser, 10).until(
        lambda b: b.find_element(
            By.CSS_SELECTOR, "input[aria-label='Edit task title']"
        )
    )
    field.clear()
    field.send_keys(text)
