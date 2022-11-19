import time

from ui.pages.base_page import BasePage
from ui.locators.main_page_locators import MainPageLocators
from selenium.webdriver.support import expected_conditions as ES
from selenium.webdriver.common.by import By
import random
import re


class MainPage(BasePage):
    locators = MainPageLocators()

    def random_items(self, locator, num=1):
        """
        Возвращает num-рандомных элементов из списка
        :param locator : tuple - Локатор секции
        :param num     : int - кол-во рандомных элементов
        :return        : list - Список элементов
        """
        items = self.count_items(locator)
        new_items = []
        for i in range(num):
            rand_int = random.randint(0, len(items)-1)
            self.logger.debug(f'Рандомно выбранный элемент: {rand_int+1}')
            new_items.append(items[rand_int])
        return new_items

    def count_items(self, locator, additional_locator='/article'):
        """
        Поиск элементов в секции, например пицца в общем списке или товары в корзине
        :param locator            : tuple - Локатор секции
        :param additional_locator : string - доп.локатор
        :return                   : list - Элементы в секции
        """
        new_locator = (By.XPATH, locator[1] + additional_locator)
        return self.find_elements(new_locator)

    def add_to_basket(self, title_in_dialog):
        self.logger.debug(f'Добавление товара в корзину: {title_in_dialog}')
        """
        В Google Chrome при добавлении 3 и 5 пицц происходит баг,
        на запрос возвращается 400 статус код и пицца не добавляется в корзину,
        чтобы обойти баг нужно нажимать более 1 раза (От 3 до 5 раз)

        Добавляем пиццу в корзину
        Если окно параметризации пропадает спустя 5 сек после клика - пицца была добавлена успешно
        Если окно не пропадает, мы его закрываем и пытаемся добавить следующую пиццу
        
        :param title_in_dialog : string - Наименование товара
        :return                : bool - True, если пицца была добавлена, False, если пицца не была добавлена
        """
        try:
            self.click(self.locators.ADD_TO_BASKET) # Пытаемся добавить в корзину
            self.wait(timeout=10).until(ES.invisibility_of_element_located(self.locators.PIZZA_DIALOG)) # Ждем когда окно параметризации пропадет
            self.logger.debug(f'Товар был добавлен в корзину: {title_in_dialog}')
            return True
        except:
            parametrize_pizza = self.find_element(self.locators.PIZZA_DIALOG)
            close = self.find_child_element(parametrize_pizza, self.locators.PARAMETRIZE_PIZZA["close_icon"])
            close.click() # Закрываем окно параметризации (если не закрылось само)
            self.logger.debug(f'Товар не был добавлен в корзину: {title_in_dialog}')
            return False

    def current_item_data(self, items):
        """
        Возвращает название и цену пиццы из главного меню (то, что указано в карточке товара)
        :return : dict - Словарь с названиями и ценами
        """
        data_items = {
            "titles": [],
            "prices": []
        }
        for item in items:
            pizza_title = item.find_element(*self.locators.MAIN_MENU["title_item"]).text
            pizza_title = re.search(r'(\w+.*\w+\!?)', pizza_title).group(0)
            pizza_price = item.find_element(*self.locators.MAIN_MENU["price_item"]).text
            pizza_price = int(re.search(r'\d+', pizza_price).group(0))
            data_items["titles"].append(pizza_title)
            data_items["prices"].append(pizza_price)
        return data_items

    def get_total_sum(self):
        """
        Возвращает полную сумму из корзины
        :return : string - Полная сумма товаров
        """
        elem = self.find_element(self.locators.BASKET["total_sum"])
        total_sum = re.findall(r'\d+', elem.get_attribute('textContent'))
        self.logger.debug(f'Получение полной суммы: {"".join(total_sum)}')
        return ''.join(total_sum)

    def delete_from_basket(self):
        """
        Удаляет лишние элементы из корзины, например подарки
        :return:
        """
        self.click(self.locators.BASKET["button_basket"]) # Открываем корзину
        items = self.count_items(self.locators.BASKET["items"]) # Находим все элементы
        for item in items:
            self.move_to_element(item)
            # Получаем цену каждого элемента
            price = self.find_child_element(item, self.locators.BASKET["item_price"]).get_attribute('textContent')
            price = int(re.search(r'\d+', price).group(0))
            # Если цена = 0 (подарок например) - удаляем из корзины
            if price == 0:
                delete_button = self.find_child_element(item, self.locators.BASKET["delete_item"])
                bottom = self.find_element(self.locators.BASKET["total_sum"])
                self.move_to_element(bottom)
                self.driver.implicitly_wait(10)
                delete_button.click() # Удаляем из корзины
        self.click(self.locators.BASKET["basket_close"])
        return self.wait(timeout=10).until(ES.invisibility_of_element_located(self.locators.BASKET["items"]))

    def items_from_basket(self):
        """
        Собирает названия товаров, добавленных в корзину, игнорирует подарки
        :return : list - Массив названий товаров
        """
        self.click(self.locators.BASKET["button_basket"])
        items = self.count_items(self.locators.BASKET["items"])
        titles = []
        for item in items:
            # Получаем цену каждого элемента
            price = self.find_child_element(item, self.locators.BASKET["item_price"]).get_attribute('textContent')
            price = int(re.search(r'\d+', price).group(0))
            # Если цена = 0 (подарок например), то пропускаем, т.к. даже после удаления (в функции delete_from_basket)
            # из корзины товары полностью не пропадают
            if price == 0:
                continue
            title = self.find_child_element(item, self.locators.BASKET["item_title"]).get_attribute('innerText')
            count = self.find_child_element(item, self.locators.BASKET["item_count"]).get_attribute('textContent') # Кол-во товара
            titles.extend([title]*int(count)) # В список добавляем каждый товар в том кол-ве, в котором он присутствует в корзине
        return titles

    def half_pizza(self, card):
        """
        Обрабатывает добавление пицц, состоящих из половинок

        :param card : Карточка товара
        :return     : list - Массив названий товаров / False - Если товар не был добавлен
        """
        card.click() # Нажимаем на карточку товара
        items = self.count_items(self.locators.HALF_PIZZA_WINDOW["halves"], additional_locator='') # Получаем все половинки
        indexes = [random.randint(0, len(items)-1) for _ in range(2)] # Берем 2 рандомных индекса половинок
        # Половинки не могут повторяться
        while indexes[0] == indexes[1]:
            indexes[1] = random.randint(0, len(items)-1)
        indexes = sorted(indexes)
        full_title = []
        for ind in indexes:
            # Добавляем название половинки в список, нажимаем на половинку
            half = items[ind]
            self.move_to_element(half)
            title = self.find_child_element(half, self.locators.HALF_PIZZA_WINDOW["title"]).text
            full_title.append(title)
            half.click()
        price = self.find_element(self.locators.PARAMETRIZE_PIZZA["price_pizza"]).text
        # Если пицца из половинок добавилась, возвращаем название пиццы, состоящее из половинок
        if self.add_to_basket(' + '.join(full_title)):
            return ' + '.join(full_title), int(price)
        return False

    def add_items_count(self, items):
        """
        Добавляет переданные элементы, возвращает словарь только с теми элементами, которые были добавлены в корзину
        :param items : Список элементов
        :return      : dict - Словарь с названиями и ценами
        """
        added_items = {
            "titles": [],
            "prices": []
        }
        for item in items:
            self.move_to_element(item)
            item_title = self.current_item_data([item])["titles"][0] # Получаем название пиццы
            if item_title == 'Пицца из половинок':
                half_pizza = self.half_pizza(item)
                if half_pizza:
                    added_items["titles"].append(half_pizza[0])
                    added_items["prices"].append(half_pizza[1])
                continue
            item.click()
            try:
                self.find_element(self.locators.PARAMETRIZE_PIZZA["small_size"], timeout=10).click()
            except:
                pass
            title_in_dialog = self.find_element(self.locators.PARAMETRIZE_PIZZA["title_pizza"]).get_attribute('innerText')
            price_in_dialog = self.find_element(self.locators.PARAMETRIZE_PIZZA["price_pizza"]).get_attribute('innerText')
            price = int(re.search(r'\d+', price_in_dialog).group(0))
            if self.add_to_basket(title_in_dialog):
                added_items["titles"].append(title_in_dialog)
                added_items["prices"].append(int(price))
        self.delete_from_basket()
        return added_items

    def get_pizza_by_name(self, names):
        """
        Получаем список имен и добавляем пиццу в корзину

        :param names: Список названий пицц
        :return: list - Список цен
        """
        pizza_prices = []
        for name in names:
            if name == 'Пицца из половинок':
                item = self.find_element(self.locators.PIZZA_BY_NAME(name))
                half_pizza = self.half_pizza(item)
                if half_pizza:
                    pizza_prices.append(half_pizza[1])
                continue
            self.click(self.locators.PIZZA_SECTION) # Переходим в раздел пицц
            self.click(self.locators.PIZZA_BY_NAME(name)) # Находим пиццу по имени
            try:
                self.find_element(self.locators.PARAMETRIZE_PIZZA["small_size"], timeout=5).click()
            except:
                pass
            price = self.find_element(self.locators.PARAMETRIZE_PIZZA["price_pizza"]).get_attribute('textContent')
            if self.add_to_basket(name):
                pizza_prices.append(int(price))
        self.delete_from_basket()
        time.sleep(3)
        return pizza_prices








