from base import BaseCase
import pytest


class TestSuite(BaseCase):
    def test_case_0(self):
        current_region = self.main_page.find_element(self.main_page.locators.CURRENT_REGION).text
        pizza_count = self.main_page.count_items(self.main_page.locators.PIZZA_SECTION)
        self.logging.debug(f'Текущий регион: {current_region}.')
        self.logging.debug(f'Кол-во пицц: {pizza_count}.')
        assert "https://dodopizza.ru/moscow" in self.driver.current_url
        assert current_region == self.config["region"]
        assert len(pizza_count) == self.config["total_pizza_count"]

    @pytest.mark.usefixtures("prepare_count")
    def test_case_2(self, prepare_count):
        pizza_count = prepare_count
        rand_items = self.main_page.random_items(self.main_page.locators.PIZZA_SECTION, pizza_count)
        added_items = self.main_page.add_items_count(rand_items)
        titles, prices = added_items.values()
        try:
            count = self.main_page.find_element(self.main_page.locators.BASKET_COUNT_ITEMS).text
        except:
            count = 0
        items_in_basket = self.main_page.items_from_basket()
        self.logging.debug(f'Пицца, которая была добавлена: {", ".join(titles)}')
        self.logging.debug(f'Пицца, которая есть в корзине: {", ".join(items_in_basket)}')
        assert "https://dodopizza.ru/moscow" in self.driver.current_url
        for title in titles:
            assert title in items_in_basket
        assert sum(prices) == int(self.main_page.get_total_sum())
        assert int(count) == pizza_count

    def test_case_3(self):
        pizza_names = self.config["pizza_list"]
        prices = self.main_page.get_pizza_by_name(pizza_names)
        try:
            count = self.main_page.find_element(self.main_page.locators.BASKET_COUNT_ITEMS).text
        except:
            count = 0
        items_in_basket = self.main_page.items_from_basket()
        total_sum = int(self.main_page.get_total_sum())
        self.logging.debug(f'Список пицц, которые нужно добавить: {", ".join(pizza_names)}')
        self.logging.debug(f'Пицца, которая есть в корзине: {", ".join(items_in_basket)}')
        assert "https://dodopizza.ru/moscow" in self.driver.current_url
        assert int(count) == len(pizza_names)
        for name in pizza_names:
            assert name in items_in_basket
        assert sum(prices) == total_sum
