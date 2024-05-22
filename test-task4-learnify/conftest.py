import datetime
import logging
import time

import allure
import pytest
from _pytest.fixtures import FixtureRequest
from allure_commons.types import AttachmentType
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

WAIT_TIMEOUT_S = 10

logger = logging.getLogger(__name__)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
    return rep


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
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"{request.function.__name__}-{datetime.datetime.now()}",
                attachment_type=AttachmentType.PNG,
            )
        except Exception as exc:
            print(exc)


class MainPageLocators:
    UNI_NAME_INPUT = (
        By.XPATH,
        './/*[@id="root"]/div/section/div/div/form/label[1]/input',
    )
    UNI_TAG_INPUT = (By.XPATH, './/form[contains(@class, "searchForm")]/label[2]/input')
    FIND_BUTTON = (By.XPATH, './/*[@id="root"]/div/section/div/div/form/button')
    UNIVERSITIES_LIST = (By.XPATH, './/ul[contains(@class, "universities__list")]')
    UNIVERSITY_NAME = (By.XPATH, './/p[contains(@class, "university-card__name")]/a')
    UNIVERSITY_TAGS = (By.XPATH, './/*[contains(@class, "university-card__tags")]/span')


class MainPage(BasePage):
    BASE_URL = "https://learnify.yakser.space/"

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def open(self):
        logger.info("Open learnify main page")
        self.driver.get(self.BASE_URL)

    def filter_by_name(self, name):
        input = self.driver.find_element(*MainPageLocators.UNI_NAME_INPUT)
        input.send_keys(name)
        time.sleep(1)
        button = self.driver.find_element(*MainPageLocators.FIND_BUTTON)
        button.click()

    def get_universities(self):
        universities = self.driver.find_element(
            *MainPageLocators.UNIVERSITIES_LIST
        ).find_elements(By.CSS_SELECTOR, "li")
        self._log_universities(universities)
        return universities

    def get_university_name(self, university):
        return university.find_element(*MainPageLocators.UNIVERSITY_NAME)

    def add_filter_tag(self, tag):
        input = self.driver.find_element(*MainPageLocators.UNI_TAG_INPUT)
        input.send_keys(tag)
        input.send_keys(keys.Keys.RETURN)
        time.sleep(1)

    def get_university_tags(self, university):
        return university.find_elements(*MainPageLocators.UNIVERSITY_TAGS)

    def _log_universities(self, universities):
        for i, uni in enumerate(universities, 1):
            formatted_tags = ", ".join(
                tag.text for tag in self.get_university_tags(uni)
            )
            logger.info(f"{i}\t{self.get_university_name(uni).text}\t{formatted_tags}")
