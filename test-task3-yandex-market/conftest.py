import datetime
import time

from allure_commons.types import AttachmentType
import allure
import pytest
from _pytest.fixtures import FixtureRequest
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

type Second = int
WAIT_TIMEOUT: Second = 10


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
        self.wait = WebDriverWait(self.driver, WAIT_TIMEOUT)


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
    CATALOG_BUTTON = (By.CSS_SELECTOR, '[data-zone-name="catalog"]')
    CATEGORIES_LIST = (By.CSS_SELECTOR, '[data-zone-name="catalog-content"]')
    CATEGORIES_LINKS = (By.CSS_SELECTOR, '/html/body/div[3]/div/div/div/div/div/div/div[1]/div/ul')
    LAPTOPS_PAGE_TITLE = (By.CSS_SELECTOR, 'h1')


class MainPage(BasePage):
    BASE_URL = "https://market.yandex.ru/"

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @allure.step('Open main page')
    def open(self):
        print('Open Yandex Market main page')
        self.driver.get(self.BASE_URL)

    @allure.step('Open laptops catalog')
    def open_laptops_catalog(self):
        print('Open laptops catalog')
        time.sleep(2)
        self.wait.until(ec.presence_of_element_located(MainPageLocators.CATALOG_BUTTON)).click()

        for span in self.wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-zone-name="catalog-content"] li[data-zone-name="category-link"] span'))):
            if span.text == 'Ноутбуки и компьютеры':
                span.click()
                break

        laptops_link = self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div[data-zone-name="item"]')))
        laptops_link.click()

        self.log_first_five_products()

    def get_page_h1(self):
        return self.wait.until(ec.presence_of_element_located(MainPageLocators.LAPTOPS_PAGE_TITLE))

    def log_first_five_products(self):
        time.sleep(1)
        products = self.wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, '.SerpLayout div[data-apiary-widget-name="@marketfront/SerpEntity"]')))
        time.sleep(1)
        count = 0
        for p in products:
            # пропускаем элемент, если это не товар, а карусель с несколькими товарами
            try:
                # p.find_element(By.CSS_SELECTOR,
                # 'div[data-apiary-widget-name="@marketfront/ModelGalleryWithHorizontalSnippetsIncut"]')
                p.find_element(By.CSS_SELECTOR, 'h3[data-zone-name="header"]')
            except exceptions.NoSuchElementException:
                name = p.find_element(By.CSS_SELECTOR, 'h3')
                price = p.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div/div/div[1]/div/div/div[5]/div/div/div/div/div/div/div/div[5]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/article/div/div/div/div/div[3]/div[2]/div/div/div/a/span/div/span[1]/span[1]')  # noqa: E501
                is_resale = False
                try:
                    p.find_element(By.CSS_SELECTOR, 'div[data-zone-name="resale-badge"]')
                    is_resale = True
                except Exception:
                    pass

                print(count + 1, name.text, price.text, f"Уценка: {is_resale}", sep='; ')
                count += 1
            if count == 5:
                break
            # time.sleep(111)

    @allure.step('Show only resale products')
    def show_resale_products(self):
        print('Show only resale products')
        self.driver.execute_script("window.scrollTo(0, 1080)")
        resale_filter = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div/div/div[1]/div/div/div[5]/div/div/div/div/div/aside/div/div[3]/div/div/div/div/div[6]/div/fieldset/div/div/div/div/div/div[2]')
        resale_filter.click()

        # time.sleep(11111)
        time.sleep(2)
        products = self.wait.until(ec.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '.SerpLayout div[data-apiary-widget-name="@marketfront/SerpEntity"]')))

        count = 0
        for p in products:
            # пропускаем элемент, если это не товар, а карусель с несколькими товарами
            try:
                # p.find_element(By.CSS_SELECTOR, 'div[data-apiary-widget-name="@marketfront/ModelGalleryWithHorizontalSnippetsIncut"]')
                p.find_element(By.CSS_SELECTOR, 'h3[data-zone-name="header"]')
            except exceptions.NoSuchElementException:
                name = p.find_element(By.CSS_SELECTOR, 'h3')
                price = p.find_element(By.XPATH,
                                       '/html/body/div[1]/div/div[4]/div/div/div[1]/div/div/div[5]/div/div/div/div/div/div/div/div[5]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/article/div/div/div/div/div[3]/div[2]/div/div/div/a/span/div/span[1]/span[1]')
                is_resale = False
                try:
                    p.find_element(By.CSS_SELECTOR, 'div[data-zone-name="resale-badge"]')
                    is_resale = True
                except:
                    pass

                assert is_resale is True

                print(count + 1, name.text, price.text, f"Уценка: {is_resale}", sep='; ')
                count += 1
            if count == 10:
                break
