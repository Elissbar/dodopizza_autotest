from base import BaseCase
import pytest


class TestSuite(BaseCase):

    def test_case_0(self):
        self.logging.debug(f'Проверка соотвествия страницы')
        assert self.driver.current_url == "https://dodopizza.ru/moscow"
        self.logging.debug(f'Переход в раздел: "Пицца"')
        self.main_page.find_element(self.main_page.locators.NAV_BAR["Пицца"]).click()
        current_region = self.main_page.find_element(self.main_page.locators.CURRENT_REGION).text
        pizza_count = self.main_page.count_items(self.main_page.locators.PIZZA_SECTION)
        self.logging.debug(f'Подсчет кол-ва товаров в разделе "Пицца": {pizza_count}')
        self.logging.debug(f'Проверка соотвествия кол-ва и региона.')
        assert current_region == self.config["region"]
        assert len(pizza_count) == self.config["total_pizza_count"]

    def test_case_1(self):
        pizza_count = 1
        assert self.driver.current_url == "https://dodopizza.ru/moscow"
        self.main_page.find_element(self.main_page.locators.NAV_BAR["Пицца"]).click()
        rand_items = self.main_page.random_items(self.main_page.locators.PIZZA_SECTION, '', pizza_count) # Получаем рандомное кол-во элементов (Пицц)
        selected_items = self.main_page.current_item_data(rand_items) # Получаем название и цену выбранных товаров (В главном меню)
        selected_titles = [title[0] for title in selected_items]
        added_items = self.main_page.add_items_count(rand_items) # Получаем те товары, которые были добавлены в корзину
        titles = [title[0] for title in added_items]
        basket = self.main_page.find_element(self.main_page.locators.BASKET_COUNT_ITEMS).text
        assert int(basket) == pizza_count
        for title in titles: # Проверяем что добавлены все те элементы, что хранятся в переменной selected_items
            assert title in selected_titles


    def test_case_2(self):
        pizza_count = self.config["add_pizza_count"]
        assert self.driver.current_url == "https://dodopizza.ru/moscow"
        self.main_page.find_element(self.main_page.locators.NAV_BAR["Пицца"]).click()
        rand_items = self.main_page.random_items(self.main_page.locators.PIZZA_SECTION, pizza_count) # Получаем рандомное кол-во элементов (Пицц)
        added_items = self.main_page.add_items_count(rand_items) # Добавляем рандомное кол-во элементов (Пицц) в корзину
        titles = [title[0] for title in added_items]
        prices = [int(title[1]) for title in added_items]
        count = self.main_page.find_element(self.main_page.locators.BASKET_COUNT_ITEMS).text
        items_in_basket = self.main_page.items_from_basket()
        for title in titles:
            assert title in items_in_basket
        assert sum(prices) == int(self.main_page.get_total_sum())
        assert int(count) == pizza_count

    def test_case_3(self):
        pizza_names = self.config["pizza_list"]
        assert self.driver.current_url == "https://dodopizza.ru/moscow"
        self.main_page.find_element(self.main_page.locators.NAV_BAR["Пицца"]).click()
        prices = [int(price) for price in self.main_page.get_pizza_by_name(pizza_names)]
        basket = self.main_page.find_element(self.main_page.locators.BASKET_COUNT_ITEMS).text
        self.logging.debug(f'Получение кол-ва товаров в корзине: {basket}')
        items = self.main_page.items_from_basket()
        self.logging.debug(f'Получение самих товаров из корзине: {items}')
        total_sum = int(self.main_page.get_total_sum())
        self.logging.debug(f'Проверка результатов')
        assert int(basket) == len(pizza_names)
        for name in pizza_names:
            assert name in items
        assert sum(prices) == total_sum
