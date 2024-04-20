import datetime
import time
from allure_commons.types import AttachmentType
import allure
import pytest
from _pytest.fixtures import FixtureRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

WAIT_TIMEOUT_S = 10


class BasePage:
    BASE_URL = "https://<empty>"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, WAIT_TIMEOUT_S)


@pytest.fixture(name="main_page")
def main_page_fixture(request: FixtureRequest, driver: WebDriver):
    main_page = MainPage(driver)
    yield main_page

    driver = main_page.driver
    if request.node.rep_call.failed:
        try:
            allure.attach(driver.get_screenshot_as_png(),
                          name=f"{request.function.__name__}-{datetime.datetime.now()}",
                          attachment_type=AttachmentType.PNG)
        except Exception as exc:
            print(exc)


class MainPageLocators:
    GO_TO_TIMETABLE_BUTTON = (By.XPATH, '//a[@href=\"/obuchauschimsya/raspisaniya/\"]')
    TIMETABLE_LINK = (
        By.XPATH, '//a[@href="https://rasp.dmami.ru/" and contains(@class, "btn") and contains(@class, "text-button")]')
    GROUP_INPUT = (By.CSS_SELECTOR, '.header.not-print > div.header-search.search > input')
    GROUPS_LIST = (By.CSS_SELECTOR, '.found-groups')
    TODAY_SCHEDULE = (By.CSS_SELECTOR, '.schedule-day_today')
    WEEK_SCHEDULE = (By.CSS_SELECTOR, '.schedule-day')


class MainPage(BasePage):
    BASE_URL = "https://mospolytech.ru"

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @allure.step('Open main page')
    def open(self):
        self.driver.get(self.BASE_URL)

    @allure.step('Open timetable section')
    def go_to_timetable_section(self):
        time.sleep(1)
        self.wait.until(ec.element_to_be_clickable(MainPageLocators.GO_TO_TIMETABLE_BUTTON)).click()

    @allure.step('Click timetable link')
    def click_timetable_link(self):
        self.wait.until(ec.element_to_be_clickable(MainPageLocators.TIMETABLE_LINK)).click()

    def find_groups_by_number(self, group_number: str):
        self.wait.until(ec.element_to_be_clickable(MainPageLocators.GROUP_INPUT)).send_keys(group_number)
        time.sleep(1)
        groups_ul = self.wait.until(ec.presence_of_element_located(MainPageLocators.GROUPS_LIST))
        return groups_ul

    def get_today_schedule(self):
        return self.wait.until(ec.presence_of_element_located(MainPageLocators.TODAY_SCHEDULE))

    def get_week_schedule(self):
        return self.driver.find_elements(By.CSS_SELECTOR, '.schedule-day')

    def get_groups_list(self, groups_element):
        return groups_element.find_elements(By.CSS_SELECTOR, '.group')

    def find_group_element_by_number(self, groups_element, group_number):
        return groups_element.find_element(By.ID, group_number)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
    return rep
