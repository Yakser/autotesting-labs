import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

BASE_URL = 'https://lambdatest.github.io/sample-todo-app'


@pytest.fixture(name="find_nth_checkbox")
def find_nth_checkbox_fixture():
    def find_nth_checkbox(selenium: WebDriver, n: int) -> WebElement:
        return selenium.find_element(By.CSS_SELECTOR, f"ul li:nth-child({n}) input[type=checkbox]")

    return find_nth_checkbox


@pytest.fixture(name="get_text_remaining")
def get_text_remaining_fixture():
    def get_text_remaining(selenium: WebDriver) -> str:
        return selenium.find_element(By.CLASS_NAME, "ng-binding").text

    return get_text_remaining


def test_header_text(selenium: WebDriver):
    selenium.get(BASE_URL)
    element = selenium.find_element(By.CSS_SELECTOR, "h2")
    assert element.text == "LambdaTest Sample App"


def test_text_remaining(selenium: WebDriver, get_text_remaining):
    selenium.get(BASE_URL)
    assert get_text_remaining(selenium) == "5 of 5 remaining"


def test_first_item_not_selected(selenium: WebDriver, find_nth_checkbox):
    selenium.get(BASE_URL)
    element = find_nth_checkbox(selenium, 1)
    assert not element.get_attribute("checked")


def test_click_todos(selenium: WebDriver, find_nth_checkbox):
    selenium.get(BASE_URL)
    for checkbox in selenium.find_elements(By.CSS_SELECTOR, "ul input[type=checkbox]"):
        checkbox.click()
        assert checkbox.get_attribute("checked")


def test_add_new_todo_item(selenium: WebDriver, find_nth_checkbox, get_text_remaining):
    new_item_content = "New Item"

    selenium.get(BASE_URL)
    selenium.find_element(By.ID, "sampletodotext").send_keys(new_item_content)
    selenium.find_element(By.ID, "addbutton").click()

    added_checkbox = find_nth_checkbox(selenium, 6)
    assert not added_checkbox.get_attribute("checked")
    assert get_text_remaining(selenium) == "6 of 6 remaining"

    added_checkbox.click()
    assert added_checkbox.get_attribute("checked")
    assert get_text_remaining(selenium) == "5 of 6 remaining"
