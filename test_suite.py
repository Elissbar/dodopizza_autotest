from base import BaseCase
import pytest


class TestSuite(BaseCase):

    def test_case_0(self):
        self.logging.debug(f'Проверка соотвествия страницы')
        assert self.driver.current_url == "https://dodopizza.ru/moscow"
        self.logging.debug(f'Переход в раздел: "Пицца"')
        self.main_page.find_element(self.main_page.locators.NAV_BAR["Пицца"]).click()
        current_region = self.main_page.find_element(self.main_page.locators.CURRENT_REGION).text
        self.logging.debug(f'Подсчет кол-ва товаров в разделе "Пицца"')
        pizza_count = self.main_page.count_items(self.main_page.locators.PIZZA_SECTION)[0]
        self.logging.debug(f'Проверка соотвествия кол-ва и региона')
        assert current_region == self.config["region"]
        assert pizza_count == self.config["total_pizza_count"]

    def test_case_1(self):
        self.logging.debug(f'Проверка соотвествия страницы')
        assert self.driver.current_url == "https://dodopizza.ru/moscow"
        self.logging.debug(f'Переход в раздел: "Пицца"')
        self.main_page.find_element(self.main_page.locators.NAV_BAR["Пицца"]).click()
        pizza_title, pizza_price, pizza_title_in_dialog, pizza_price_in_dialog = self.main_page.get_random_item(self.main_page.locators.PIZZA_SECTION)
        basket = self.main_page.find_element(self.main_page.locators.BASKET_COUNT_ITEMS).text
        self.logging.debug(f'Проверка результатов')
        assert pizza_title == pizza_title_in_dialog
        assert pizza_price == pizza_price_in_dialog
        assert int(basket) == 1

    # @pytest.mark.xfail
    def test_case_2(self):
        pizza_count = self.config["add_pizza_count"]
        self.logging.debug(f'Проверка соотвествия страницы')
        assert self.driver.current_url == "https://dodopizza.ru/moscow"
        self.logging.debug(f'Переход в раздел: "Пицца"')
        self.main_page.find_element(self.main_page.locators.NAV_BAR["Пицца"]).click()
        names, prices = self.main_page.get_number_pizza(self.main_page.locators.PIZZA_SECTION, pizza_count)
        count = self.main_page.find_element(self.main_page.locators.BASKET_COUNT_ITEMS).text
        items = self.main_page.items_from_basket()
        self.logging.debug(f'Проверка результатов')
        for name in names:
            assert name in items
        assert sum(prices) == int(self.main_page.get_total_sum())
        assert int(count) == pizza_count

    def test_case_3(self):
        pizza_names = self.config["pizza_list"]
        assert self.driver.current_url == "https://dodopizza.ru/moscow"
        self.main_page.find_element(self.main_page.locators.NAV_BAR["Пицца"]).click()
        prices = [int(price) for price in self.main_page.get_pizza_by_name(pizza_names)]
        basket = self.main_page.find_element(self.main_page.locators.BASKET_COUNT_ITEMS).text
        items = self.main_page.items_from_basket()
        total_sum = int(self.main_page.get_total_sum())
        self.logging.debug(f'Проверка результатов')
        for name in pizza_names:
            assert name in items
        assert sum(prices) == total_sum
        assert int(basket) == len(pizza_names)
