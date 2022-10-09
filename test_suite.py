from base import BaseCase


class TestSuite(BaseCase):

    def test_case_0(self):
        self.main_page.choose_region()
        assert self.driver.current_url == "https://dodopizza.ru/moscow"
        self.main_page.go_to_section("Пицца")
        current_region = self.main_page.get_region()
        pizza_count = self.main_page.count_items(self.main_page.locators.PIZZA_SECTION)[0]
        assert pizza_count == self.config["total_pizza_count"]
        assert current_region == self.config["region"]

    def test_case_1(self):
        self.main_page.choose_region()
        assert self.driver.current_url == "https://dodopizza.ru/moscow"
        self.main_page.go_to_section("Пицца")
        pizza_title, pizza_price, pizza_title_in_dialog, pizza_price_in_dialog = self.main_page.get_random_item(self.main_page.locators.PIZZA_SECTION)
        assert pizza_title == pizza_title_in_dialog
        assert pizza_price == pizza_price_in_dialog
        basket = self.main_page.find_element(self.main_page.locators.NAVBAR_BASKET).text
        assert int(basket) >= 1

    def test_case_2(self):
        pizza_count = self.config["add_pizza_count"]
        self.main_page.choose_region()
        assert self.driver.current_url == "https://dodopizza.ru/moscow"
        self.main_page.go_to_section("Пицца")
        pizza_list = self.main_page.get_number_pizza(self.main_page.locators.PIZZA_SECTION, pizza_count)
        pizza_names = [name[0] for name in pizza_list]
        total_price = [int(name[1]) for name in pizza_list]
        basket = self.main_page.find_element(self.main_page.locators.NAVBAR_BASKET).text
        assert int(basket) >= pizza_count
        self.main_page.open_basket()
        items = self.main_page.items_from_basket()
        for name in pizza_names:
            assert name in items
        assert sum(total_price) == int(self.main_page.get_total_sum())

    def test_case_3(self):
        pizza_names = self.config["pizza_list"]
        self.main_page.choose_region()
        assert self.driver.current_url == "https://dodopizza.ru/moscow"
        self.main_page.go_to_section("Пицца")
        prices = [int(price) for price in self.main_page.get_pizza_by_name(pizza_names)]
        basket = self.main_page.find_element(self.main_page.locators.NAVBAR_BASKET).text
        assert int(basket) >= len(pizza_names)
        self.main_page.open_basket()
        items = self.main_page.items_from_basket()
        for name in pizza_names:
            assert name in items
        total_sum = int(self.main_page.get_total_sum())
        assert sum(prices) == total_sum









