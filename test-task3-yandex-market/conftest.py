import datetime
import logging
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
            logger.error(exc)


class MainPageLocators:
    CATALOG_BUTTON = (By.CSS_SELECTOR, '[data-zone-name="catalog"]')
    CATEGORIES_LIST = (By.CSS_SELECTOR, '[data-zone-name="catalog-content"]')
    CATEGORIES_LINKS = (
        By.CSS_SELECTOR,
        'div[data-zone-name="catalog-content"] li[data-zone-name="category-link"] span',
    )
    LAPTOPS_PAGE_TITLE = (By.CSS_SELECTOR, "h1")
    LAPTOPS_PAGE_LINK = (By.CSS_SELECTOR, 'div[data-zone-name="item"]')
    RESALE_FILTER = (
        By.CSS_SELECTOR,
        'label[data-auto="filter-list-item-resale_resale"]',
    )
    PRODUCT_ITEM = (By.CSS_SELECTOR, 'div[data-baobab-name="productSnippet"]')
    RESALE_BADGE = (By.CSS_SELECTOR, 'div[data-zone-name="resale-badge"]')
    PRODUCT_PRICE = (By.CSS_SELECTOR, 'span[data-auto="snippet-price-current"]')
    PRODUCT_NAME = (By.CSS_SELECTOR, "h3")


class MainPage(BasePage):
    BASE_URL = "https://market.yandex.ru/"

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @allure.step("Open main page")
    def open(self):
        logger.info("Open Yandex Market main page")
        self.driver.get(self.BASE_URL)

    @allure.step("Open laptops catalog")
    def open_laptops_catalog(self):
        logger.info("Open laptops catalog")
        time.sleep(2)
        self.wait.until(
            ec.presence_of_element_located(MainPageLocators.CATALOG_BUTTON)
        ).click()

        for span in self.wait.until(
            ec.presence_of_all_elements_located(MainPageLocators.CATEGORIES_LINKS)
        ):
            if span.text == "Ноутбуки и компьютеры":
                span.click()
                break

        laptops_link = self.wait.until(
            ec.presence_of_element_located(MainPageLocators.LAPTOPS_PAGE_LINK)
        )
        laptops_link.click()

        self.log_first_five_products()

    def get_page_h1(self):
        return self.wait.until(
            ec.presence_of_element_located(MainPageLocators.LAPTOPS_PAGE_TITLE)
        )

    def log_first_five_products(self):
        time.sleep(1)
        products = self.wait.until(
            ec.presence_of_all_elements_located(MainPageLocators.PRODUCT_ITEM)
        )
        time.sleep(1)
        count = 0
        for p in products:
            name = p.find_element(*MainPageLocators.PRODUCT_NAME)
            price = p.find_element(*MainPageLocators.PRODUCT_PRICE)
            is_resale = False
            try:
                p.find_element(*MainPageLocators.RESALE_BADGE)
                is_resale = True
            except Exception:
                pass

            logger.info(f"{count + 1}\t{name.text}\t{price.text}\tУценка: {is_resale}")
            count += 1
            if count == 5:
                break

    @allure.step("Show only resale products")
    def show_resale_products(self):
        logger.info("Show only resale products")
        self.driver.execute_script("window.scrollTo(0, 1080)")
        time.sleep(2)
        resale_filter = self.driver.find_element(*MainPageLocators.RESALE_FILTER)
        resale_filter.click()

        time.sleep(3)
        products = self.wait.until(
            ec.presence_of_all_elements_located(MainPageLocators.PRODUCT_ITEM)
        )
        count = 0
        for p in products:
            name = p.find_element(*MainPageLocators.PRODUCT_NAME)
            price = p.find_element(*MainPageLocators.PRODUCT_PRICE)
            is_resale = False
            try:
                p.find_element(*MainPageLocators.RESALE_BADGE)
                is_resale = True
            except Exception as exc:
                logger.error(exc)

            assert is_resale is True

            logger.info(f"{count + 1}\t{name.text}\t{price.text}\tУценка: {is_resale}")
            count += 1
            if count == 10:
                break
