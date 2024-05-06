def test_yandex_market_filters(main_page):
    main_page.open()
    assert (
        main_page.driver.title
        == "Интернет-магазин Яндекс Маркет — покупки с быстрой доставкой"
    )
    main_page.open_laptops_catalog()

    h1 = main_page.get_page_h1()
    assert h1.text.startswith("Ноутбуки")

    main_page.show_resale_products()
    assert 0
