from ui.pages.base_page import BasePage
from ui.locators.main_page_locators import MainPageLocators
from selenium.webdriver.support import expected_conditions as ES
from selenium.webdriver.common.by import By
import random
import re
import time


class MainPage(BasePage):
    locators = MainPageLocators()

    def count_items(self, locator):
        by, path = locator[0], locator[1] + '/article'
        # articles = self.driver.find_element(locator[0], locator[1]).find_elements(locator[0], './article')
        articles = self.find_elements((by, path))
        return len(articles), articles

    def choose_region(self):
        self.find_element(self.locators.CHOOSE_REGION).click()
        return

    def go_to_section(self, section):
        # self.find_element(self.locators.CHOOSE_REGION).click()
        self.find_element(self.locators.SECTIONS[section]).click()
        return

    def get_region(self):
        current_region = self.find_element(self.locators.CURRENT_REGION).text
        return current_region

    def get_random_item(self, locator):
        items = self.count_items(locator)
        current_item = items[1][random.randint(1, items[0])]
        # current_item = items[1][13]
        try:
            pizza_title = current_item.find_element(locator[0], './main/div').text # //section[@id="pizzas"]/article[4]/main/div
            pizza_price = current_item.find_element(locator[0], './footer/div[@class="product-control-price"]').text[3:6] # //section[@id="pizzas"]/article[4]/footer/div[@class="product-control-price"]
        except:
            pizza_title = current_item.find_element(locator[0], './div[@class="card-main"]/h3').text # //section[@id="pizzas"]/article[4]/main/div
            pizza_price = current_item.find_element(locator[0], './div[@class="card-main"]/button').text[:3] # //section[@id="pizzas"]/article[4]/footer/div[@class="product-control-price"]
        current_item.click()
        self.find_element(self.locators.SIZE_PIZZA).click()
        pizza_title_in_dialog = self.find_element(self.locators.TITLE_IN_DIALOG(pizza_title)).text
        pizza_price_in_dialog = self.find_element(self.locators.PRICE_IN_DIALOG).text
        self.find_element(self.locators.ADD_TO_BASKET).click()
        return pizza_title, pizza_price, pizza_title_in_dialog, pizza_price_in_dialog

    def open_basket(self):
        self.click(self.locators.BASKET)

    def get_total_sum(self):
        elem = self.find_element(self.locators.TOTAL_BASKET_SUM)
        self.move_to_element(elem)
        total_sum = re.findall('\d*', elem.get_attribute('textContent'))
        return ''.join(total_sum)
        # return self.find_element(self.locators.TOTAL_BASKET_SUM).get_attribute('textContent').replace('₽', '').replace(' ', '')

    def items_from_basket(self):
        items = self.count_items(self.locators.BASKET_WINDOW)
        # print('ITEMS in basket', items[1])
        titles = []
        for item in items[1]:
            price = self.find_child_element(item, (By.XPATH, './div[contains(@class, "-2")]/div[contains(@class, "-7")]/div')).get_attribute('textContent')
            if '0' in price:
                continue
            # print('item in for in', item)
            title = self.find_child_element(item, (By.XPATH, './div/picture/../div/h3')).get_attribute('textContent')
            count = self.find_child_element(item, (By.XPATH, './div[contains(@class, "-2")]/div[contains(@class, "-6")]/div/div')).get_attribute('textContent')
            # print('count is:', count)
            titles.extend([title]*int(count))
        return titles

    def get_number_pizza(self, locator, number):
        items = self.count_items(locator)
        # print('len', items[0])
        pizza_list = []
        for i in range(number):
            # self.click(self.locators.SECTIONS["Пицца"])
            # print(f'Go to pizza section: {i}')
            current_item = items[1][random.randint(1, items[0]-1)]
            # current_item = items[1][33]
            # print('current item:', current_item)
            # try:
                # title = current_item.find_element(locator[0], './main/div').text
                # title = self.find_child_element(current_item, (By.XPATH, './main/div')).get_attribute('textContent').strip()
            # except:
                # title = current_item.find_element(locator[0], './div[@class="card-main"]/h3').text
                # title = self.find_child_element(current_item, (By.XPATH, './div[@class="card-main"]/h3')).get_attribute('textContent').strip()
            # print(current_item.get_attribute('data-testid'))
            self.move_to_element(current_item)
            current_item.click()
            # print(f'Open card: {i}')
            title = self.find_element(self.locators.NAME_IN_CART).get_attribute('textContent')
            price = self.find_element(self.locators.PRICE_IN_DIALOG).get_attribute('textContent')
            pizza_list.append((title, price))
            self.click(self.locators.ADD_TO_BASKET)
            # print(f'Add to basket: {i}')
            while True:
                try:
                    self.wait().until(ES.invisibility_of_element_located(self.locators.PIZZA_DIALOG))
                    break
                except:
                    self.click(self.locators.ADD_TO_BASKET)
                    # print(f'Add to basket: {i}')


        return pizza_list

    def get_pizza_by_name(self, list):
        pizza_list = []
        for i in list:
            path = f'./main/div[contains(text(), "{i}")]'
            item = self.count_items(self.locators.PIZZA_SECTION)[1]
            print('ITEM:', item)
            elem = self.find_child_element(item, (By.XPATH, path))

            print(elem.get_attribute('textContent'))
            elem.click()

        time.sleep(10)








