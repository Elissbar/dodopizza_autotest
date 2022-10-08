import pytest
from ui.pages.main_page import MainPage


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, request):
        self.driver = driver
        self.main_page = MainPage(self.driver)
