import pytest
from ui.pages.main_page import MainPage
import logging


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config):
        self.driver = driver
        self.config = config
        self.logging = logging.getLogger('test')
        self.main_page = MainPage(self.driver)
