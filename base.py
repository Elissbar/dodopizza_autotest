import pytest
from ui.pages.main_page import MainPage


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, logger):
        self.driver = driver
        self.config = config
        self.logging = logger
        self.main_page = MainPage(self.driver)

    @pytest.fixture(scope='function', autouse=True)
    def open_main_page(self, setup):
        """
        Фикстура, которая автоматически срабатывает для каждого теста
        Открывает основную страницу
        """
        self.logging.debug(f'Открытие основной страницы: {self.main_page.__class__.__name__}')
        self.main_page.click(self.main_page.locators.CHOOSE_REGION(region=self.config["region"]))
