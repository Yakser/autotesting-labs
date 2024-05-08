import datetime

from selenium.webdriver.support import expected_conditions as ec


def test_timetable_opens(main_page):
    main_page.open()
    main_page.go_to_timetable_section()
    main_page.click_timetable_link()

    assert ec.number_of_windows_to_be(2)

    main_page.driver.switch_to.window(main_page.driver.window_handles[1])

    group_number = "221-322"
    groups_element = main_page.find_groups_by_number(group_number)
    groups = main_page.get_groups_list(groups_element)

    assert len(groups) == 1

    found_group = main_page.find_group_element_by_number(groups_element, group_number)
    assert found_group is not None

    found_group.click()

    assert main_page.driver.title == f"Расписание {group_number}"

    # if today is not sunday
    if datetime.datetime.now().weekday() != 6:
        today_schedule = main_page.get_today_schedule()
        assert (
            today_schedule.value_of_css_property("background-color")
            == "rgb(226, 255, 217)"
        )
    week_schedule = main_page.get_week_schedule()
    assert len(week_schedule) == 6
