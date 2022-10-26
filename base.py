import pytest
from ui.pages.main_page import MainPage


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, logger):
        self.driver = driver
        self.config = config
        self.logger = logger
        self.main_page = MainPage(self.driver)

    @pytest.fixture(scope='function', autouse=True)
    def open_main_page(self, setup):
        """
        Фикстура, которая автоматически срабатывает для каждого теста
        Открывает основную страницу
        """
        self.logger.debug(f'Открытие основной страницы: {self.main_page.__class__.__name__}')
        self.main_page.click(self.main_page.locators.CHOOSE_REGION(region=self.config["region"]))
        self.main_page.find_element(self.main_page.locators.NAV_BAR["Пицца"]).click()

    @pytest.fixture(params=[1, 'config'])
    def prepare_count(self, request):
        if request.param == 'config':
            request.param = self.config["add_pizza_count"]
        return request.param

