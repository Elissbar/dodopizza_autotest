from selenium.webdriver.common.by import By


class MainPageLocators:
    CHOOSE_REGION = (By.XPATH, '//div[contains(@class, "big-city-container")]/a[@href="/moscow"]')
    CURRENT_REGION =(By.XPATH, '//h1[@class="header__about-slogan"]/a')

    SECTIONS = {
        "Пицца": (By.XPATH, '//a[text()="Пицца"]')
    }

    PIZZA_SECTION = (By.XPATH, '//section[@id="pizzas"]')

    PIZZA_DIALOG = (By.XPATH, '//div[contains(@data-testid, "product__card")]')

    # TITLE_IN_DIALOG = (By.XPATH, '//span[contains(text(), "")]')
    # TITLE_IN_DIALOG = lambda self, x: (By.XPATH, f'//span[text() = "{x}"]')
    TITLE_IN_DIALOG = lambda self, x: (By.XPATH, f'//span[contains(text(), "{x}")]')
    NAME_IN_CART = (By.XPATH, '//span[contains(@class, "-12")]')
    PRICE_IN_DIALOG = (By.XPATH, '//button[@data-type="primary"]//span[contains(@class, "money__value")]')

    SIZE_PIZZA = (By.XPATH, '//label[@data-testid="menu__pizza_size_1"]')

    ADD_TO_BASKET = (By.XPATH, '//div[contains(@data-testid, "product__card")]//button[@data-size="big"]')

    NAVBAR_BASKET = (By.XPATH, '//div[@data-testid="navigation__cart"]/button[@data-type="primary"]//div[@data-testid="cart-button__quantity"]')
    BASKET = (By.XPATH, '//div[@data-testid="navigation__cart"]/button')

    BASKET_WINDOW = (By.XPATH, '//section[@data-testid="cart__list"]')

    # COUNT_ITEMS_IN_BASKET
    # TOTAL_BASKET_SUM = (By.XPATH, '//div[@class="price"]')
    TOTAL_BASKET_SUM = (By.XPATH, '//div[contains(text(), "Сумма заказа")]/span')
