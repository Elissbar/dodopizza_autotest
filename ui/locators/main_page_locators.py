from selenium.webdriver.common.by import By


class MainPageLocators:
    CHOOSE_REGION = lambda self, region: (By.XPATH, f'//div[contains(@class, "big-city-container")]/a[contains(text(), "{region}")]')
    CURRENT_REGION = (By.XPATH, '//span[@class="header__about-slogan"]/a') # Выбранный регион

    NAV_BAR = {
        "Пицца": (By.XPATH, '//a[text()="Пицца"]')
    }
    PIZZA_SECTION = (By.XPATH, '//section[@id="pizzas"]') # Секция с пиццой на основной странице

    BASKET = {
        "button_basket": (By.XPATH, '//div[@data-testid="navigation__cart"]/button'), # Кнопка корзины в главном меню
        "items": (By.XPATH, '//section[@data-testid="cart__list"]'), # Товары в корзине
        "item_title": (By.XPATH, './div/picture/../div/h3'), # Название товара
        "item_price": (By.XPATH, './div[contains(@class, "-2")]/div[contains(@class, "-7")]/div[@class="current"]'), # Цена товара
        "item_count": (By.XPATH, './div[contains(@class, "-2")]/div[contains(@class, "-6")]/div/div'), # Кол-во товара
        "total_sum": (By.XPATH, '//div[contains(text(), "Сумма заказа")]/span'), # Сумма заказа
        "delete_item": (By.XPATH, './button'), # Кнопка для удаления товара
        "item_after_delete": (By.XPATH, './div[contains(@class, "-8")]'),
        "basket_close": (By.XPATH, '//button[@class="button-close"]'), # Кнопка для закрытия корзины
    }
    ADD_TO_BASKET = (By.XPATH, '//button[@data-size="big"]') # Кнопка добавления товара в корзину
    BASKET_COUNT_ITEMS = (By.XPATH, '//div[@data-testid="cart-button__quantity"]') # Кол-во товаров на кнопке корзины

    MAIN_MENU = {
        "title_item": (By.XPATH, './*/*[contains(@class, "title") or contains(@data-gtm-id, "title")]'), # Название из карточки товара в основном меню
        "price_item": (By.XPATH, './*/*[@class="product-control-price" or contains(@class, "add-button")]') # Цена из карточки товара в основном меню
    }
    # Поиск пиццы по названию
    PIZZA_BY_NAME = lambda self, name: (By.XPATH, f'//*[contains(text(), "{name}")]')

    PARAMETRIZE_PIZZA = { # Окно параметризации
        "title_pizza": (By.XPATH, '//*[contains(@class, "-12")]'),
        "price_pizza": (By.XPATH, '//button[@data-type="primary"]//span[contains(@class, "_value")]'),
        "small_size": (By.XPATH, '//label[@data-testid="menu__pizza_size_1"]'),
        "close_icon": (By.XPATH, './i'),
    }
    PIZZA_DIALOG = (By.XPATH, '//*[@clip-rule="evenodd" and @fill="white"]/../../..')
    HALF_PIZZA_WINDOW = {
        "halves": (By.XPATH, '//div[contains(@class, "sc-10")]/div[contains(@class, "-2 ")]'),
        "title": (By.XPATH, './div/span/../div')
    }
