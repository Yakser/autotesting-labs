import time

import pytest


def test_filter_by_name(main_page):
    main_page.open()
    assert main_page.driver.title == "Learnify | Главная"

    filter_value = "Московский"
    main_page.filter_by_name(filter_value)
    time.sleep(0.3)

    # проверяем что все отфильтрованные университеты содержат в названии нужну подстроку
    universities = main_page.get_universities()
    for uni in universities:
        assert filter_value.lower() in main_page.get_university_name(uni).text.lower()


def test_filter_by_tags(main_page):
    main_page.open()

    tags_values = ["web", "IT"]
    for tag in tags_values:
        main_page.add_filter_tag(tag)
    time.sleep(1)

    # проверяем что все отфильтрованные университеты содержат хотя бы один нужный тег, по которым фильтровали
    universities = main_page.get_universities()
    for uni in universities:
        tags = {tag.text for tag in main_page.get_university_tags(uni)}
        assert any(tag.lower() in tags for tag in tags_values)


@pytest.skip()
def test_login_happy_path(main_page):
    main_page.open()
    # todo: проверить happy path логина


@pytest.skip()
def test_login_invalid_credentials(main_page):
    main_page.open()
    # todo: проверить, что при неверном логине или пароле в форме входа отображается соответствующая ошибка


@pytest.skip()
def test_profile_happy_path(main_page):
    main_page.open()
    # todo: авторизоваться
    # todo: зайти в профиль
    # todo: проверить, что в профиле лежат нужные данные
