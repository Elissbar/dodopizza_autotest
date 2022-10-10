from ui.pages.base_page import BasePage
from ui.locators.main_page_locators import MainPageLocators
from selenium.webdriver.support import expected_conditions as ES
from selenium.webdriver.common.by import By
import random
import re


class MainPage(BasePage):
    locators = MainPageLocators()

    def count_items(self, locator):
        """
        Ищем элементы в секции, например пицца в общем списке или товары в корзине
        :param locator:
        :return: кол-во элементов в секции, сами элементы
        """
        locator = (By.XPATH, locator[1] + '/article')
        articles = self.find_elements(locator)
        return len(articles), articles

    def add_to_basket(self):
        self.logging.debug(f'Добавление товара в корзину')
        """
        В Google Chrome при добавлении 3 и 5 пицц происходит баг,
        на запрос возвращается 400 статус код и пицца не добавляется в корзину,
        чтобы обойти баг нужно нажимать более 1 раза (От 3 до 5 раз)

        Добавляем пиццу в корзину
        Если окно параметризации пропадает спустя 5 сек после клика - пицца была добавлена
        Если окно не пропадает, мы его закрываем и пытаемся добавить следующую пиццу
        :return: bool - пицца добавилась или нет
        """
        try:
            self.click(self.locators.ADD_TO_BASKET)
            self.wait(timeout=5).until(ES.invisibility_of_element_located(self.locators.PIZZA_DIALOG))
            self.logging.debug(f'Товар был добавлен в корзину')
            return True
        except:
            parametrize_pizza = self.find_element(self.locators.PIZZA_DIALOG)
            close = self.find_child_element(parametrize_pizza, self.locators.PARAMETRIZE_PIZZA["close_icon"])
            close.click()
            self.logging.debug(f'Товар не был добавлен в корзину')
            return False

    def current_item_data(self, current_item):
        """
        Возвращает название и цену пиццы из главного меню (то, что указано в карточке товара)
        :return: (title, price)
        """
        try:
            pizza_title = current_item.find_element(*self.locators.MAIN_MENU["common_pizza_title"]).text
            pizza_price = current_item.find_element(*self.locators.MAIN_MENU["common_pizza_price"]).text[3:6]
        except:
            pizza_title = current_item.find_element(*self.locators.MAIN_MENU["special_pizza_title"]).text
            pizza_price = current_item.find_element(*self.locators.MAIN_MENU["special_pizza_price"]).text[:3]
        return pizza_title, pizza_price

    def get_total_sum(self):
        """
        Возвращаем полную сумму из корзины
        :return: total_sum - полная сумма
        """
        elem = self.find_element(self.locators.BASKET["total_sum"])
        total_sum = re.findall(r'\d+', elem.get_attribute('textContent'))
        self.logging.debug(f'Получение полной суммы: {"".join(total_sum)}')
        return ''.join(total_sum)

    def delete_from_basket(self):
        """
        Удаляет лишние элементы из корзины, например подарки
        :return:
        """
        self.click(self.locators.BASKET["button_basket"])
        items = self.count_items(self.locators.BASKET["items"])
        for item in items[1]:
            self.move_to_element(item)
            price = self.find_child_element(item, self.locators.BASKET["item_price"]).get_attribute('textContent')
            if '0' in price:
                delete_button = self.find_child_element(item, self.locators.BASKET["delete_item"])
                bottom = self.find_element(self.locators.BASKET["total_sum"])
                self.move_to_element(bottom)
                self.driver.implicitly_wait(10)
                delete_button.click()
        self.click(self.locators.BASKET["basket_close"])

    def items_from_basket(self):
        """
        Собирает названия товаров, добавленных в корзину, игнорирует подарки
        :return: list - массив названий товаров
        """
        self.click(self.locators.BASKET["button_basket"])
        items = self.count_items(self.locators.BASKET["items"])
        titles = []
        for item in items[1]:
            price = self.find_child_element(item, self.locators.BASKET["item_price"]).get_attribute('textContent')
            if '0' in price:
                continue
            title = self.find_child_element(item, self.locators.BASKET["item_title"]).get_attribute('textContent').strip()
            count = self.find_child_element(item, self.locators.BASKET["item_count"]).get_attribute('textContent')
            titles.extend([title]*int(count))
        return titles

    def get_random_item(self, locator):
        """
        Выбираем рандомную пиццу из общего списка
        В тест возвращаем название и цену пиццы из главного меню, а также название и цену пиццы из окна параметризации
        :param locator:
        :return: tuple - (название из главного меню, цена из главного меню, название из окна, цена из окна)
        """
        items = self.count_items(locator)
        curr_int = random.randint(1, items[0]-1)
        while curr_int == 3:
            curr_int = random.randint(1, items[0]-1)
        current_item = items[1][curr_int]
        self.move_to_element(current_item)
        pizza_title, pizza_price = self.current_item_data(current_item)
        current_item.click()
        try:
            self.find_element(self.locators.PARAMETRIZE_PIZZA["pizza_size"], timeout=2).click()
        except:
            pass
        pizza_title = re.findall(r'\w+\-*\w*\!*', pizza_title)
        pizza_title = ' '.join(pizza_title)
        pizza_title_in_dialog = self.find_element(self.locators.PARAMETRIZE_PIZZA["title_pizza"]).text # Название пиццы в окне параметризации
        pizza_price_in_dialog = self.find_element(self.locators.PARAMETRIZE_PIZZA["price_pizza"]).text # Цена пиццы в окне параметризации
        self.add_to_basket()
        self.delete_from_basket()
        return pizza_title, pizza_price, pizza_title_in_dialog, pizza_price_in_dialog

    def get_number_pizza(self, locator, number):
        """
        Добавление определенного кол-ва пицц в корзину
        :param locator:
        :param number:
        :return: pizza_list - список кортежей с названием и ценой добавленных пицц
        """
        items = self.count_items(locator)
        titles = []
        prices = []
        for i in range(number):
            current_item = items[1][random.randint(1, items[0]-1)]
            self.move_to_element(current_item)
            current_item.click()
            title = self.find_element(self.locators.PARAMETRIZE_PIZZA["title_pizza"]).get_attribute('textContent') # Название пиццы в окне параметризации
            title = re.findall(r'\w+\-*\w*\!*', title)
            title = ' '.join(title)
            price = self.find_element(self.locators.PARAMETRIZE_PIZZA["price_pizza"]).get_attribute('textContent') # Цена пиццы в окне параметризации
            if self.add_to_basket():
                titles.append(title)
                prices.append(int(price))
        self.delete_from_basket()
        return titles, prices

    def get_pizza_by_name(self, list):
        """
        Получаем список имен и добавляем пиццу в корзину
        :param list:
        :return:
        """
        pizza_prices = []
        for name in list:
            self.click(self.locators.PIZZA_SECTION)
            try:
                self.click(self.locators.COMMON_BY_NAME(name))
                self.find_element(self.locators.PARAMETRIZE_PIZZA["pizza_size"], timeout=2).click()
            except:
                self.click(self.locators.SPECIAL_BY_NAME(name))
            price = self.find_element(self.locators.PARAMETRIZE_PIZZA["price_pizza"]).get_attribute('textContent')
            if self.add_to_basket():
                pizza_prices.append(price)
        self.delete_from_basket()
        return pizza_prices








