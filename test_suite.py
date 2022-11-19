from base import BaseCase
import pytest


class TestSuite(BaseCase):
    def test_items_in_section(self):
        current_region = self.main_page.find_element(self.main_page.locators.CURRENT_REGION).text # Получаем выбранный регион
        pizza_count = self.main_page.count_items(self.main_page.locators.PIZZA_SECTION) # Считаем кол-во пицц в секции
        assert "https://dodopizza.ru/moscow" in self.driver.current_url
        assert current_region == self.config["region"]
        self.logger.debug(f'Текущий регион: {current_region}. Ожидаемый регион: {self.config["region"]}')
        assert len(pizza_count) == self.config["total_pizza_count"]
        self.logger.debug(f'Ожидаемое кол-во: {self.config["total_pizza_count"]}. Фактическое кол-во: {len(pizza_count)}')

    @pytest.mark.usefixtures("prepare_count")
    def test_add_to_basket(self, prepare_count):
        pizza_count = prepare_count # Получаем кол-во пицц из параметров
        # Выбираем несколько рандомных элементов в секции
        rand_items = self.main_page.random_items(self.main_page.locators.PIZZA_SECTION, pizza_count)
        added_items = self.main_page.add_items_count(rand_items) # Добавляем выбранные элементы в корзину
        titles, prices = added_items.values() # Получаем названия и цены выбранных элементов
        try:
            # Получаем кол-во элементов в корзине (на кнопке в основном меню)
            count = self.main_page.find_element(self.main_page.locators.BASKET_COUNT_ITEMS).text
        except:
            count = 0
        items_in_basket = self.main_page.items_from_basket() # Получаем товары в корзине
        self.logger.debug(f'Пицца, которая была добавлена: {", ".join(titles)}')
        self.logger.debug(f'Пицца, которая есть в корзине: {", ".join(items_in_basket)}')
        assert "https://dodopizza.ru/moscow" in self.driver.current_url
        for title in titles:
            assert title in items_in_basket
        assert sum(prices) == int(self.main_page.get_total_sum())
        assert int(count) == pizza_count

    def test_add_by_pizza_name(self):
        pizza_names = self.config["pizza_list"] # Получаем название пицц
        prices = self.main_page.get_pizza_by_name(pizza_names) # Получаем список цен добавленных пицц
        try:
            count = self.main_page.find_element(self.main_page.locators.BASKET_COUNT_ITEMS).text
        except:
            count = 0
        items_in_basket = self.main_page.items_from_basket() # Получаем товары в корзине
        total_sum = int(self.main_page.get_total_sum()) # Получаем полную стоимость заказа
        self.logger.debug(f'Список пицц, которые нужно добавить: {", ".join(pizza_names)}')
        self.logger.debug(f'Пицца, которая есть в корзине: {", ".join(items_in_basket)}')
        assert "https://dodopizza.ru/moscow" in self.driver.current_url
        assert int(count) == len(pizza_names)
        for name in pizza_names:
            assert name in items_in_basket
        assert sum(prices) == total_sum
