from selenium.webdriver.common.by import By


class MainPageLocators:
    CHOOSE_REGION = lambda self, region: (By.XPATH, f'//div[contains(@class, "big-city-container")]/a[contains(text(), "{region}")]')
    CURRENT_REGION = (By.XPATH, '//h1[@class="header__about-slogan"]/a')

    NAV_BAR = {
        "Пицца": (By.XPATH, '//a[text()="Пицца"]')
    }
    PIZZA_SECTION = (By.XPATH, '//section[@id="pizzas"]')

    BASKET = {
        "button_basket": (By.XPATH, '//div[@data-testid="navigation__cart"]/button'),
        "items": (By.XPATH, '//section[@data-testid="cart__list"]'),
        "item_title": (By.XPATH, './div/picture/../div/h3'),
        "item_price": (By.XPATH, './div[contains(@class, "-2")]/div[contains(@class, "-7")]/div'),
        "item_count": (By.XPATH, './div[contains(@class, "-2")]/div[contains(@class, "-6")]/div/div'),
        "total_sum": (By.XPATH, '//div[contains(text(), "Сумма заказа")]/span'),
        "delete_item": (By.XPATH, './button'),
        "basket_close": (By.XPATH, '//button[@class="button-close"]'),
    }
    ADD_TO_BASKET = (By.XPATH, '//div[contains(@data-testid, "product__card")]//button[@data-size="big"]')
    BASKET_COUNT_ITEMS = (By.XPATH, '//div[@data-testid="cart-button__quantity"]')

    MAIN_MENU = {
        "common_pizza_title": (By.XPATH, './main/div'),
        "common_pizza_price": (By.XPATH, './footer/div'),
        "special_pizza_title": (By.XPATH, './div/h3'),
        "special_pizza_price": (By.XPATH, './div/button'),
    }
    COMMON_BY_NAME = lambda self, name: (By.XPATH, f'//main/div[contains(text(), "{name}")]')
    SPECIAL_BY_NAME = lambda self, name: (By.XPATH, f'//div[@class="card-main"]/h3[contains(text(), "{name}")]/../../div')


    PARAMETRIZE_PIZZA = {
        "title_pizza": (By.XPATH, '//span[contains(@class, "-12")]'),
        "price_pizza": (By.XPATH, '//button[@data-type="primary"]//span[contains(@class, "money__value")]'),
        "pizza_size": (By.XPATH, '//label[@data-testid="menu__pizza_size_1"]'),
        "close_icon": (By.XPATH, './../i')
    }
    PIZZA_DIALOG = (By.XPATH, '//div[contains(@data-testid, "product__card")]')
