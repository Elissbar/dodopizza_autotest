import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os


@pytest.fixture(scope='session')
def config(request):
    url = 'https://dodopizza.ru/'
    return {'url': url}


@pytest.fixture(scope='function')
def driver(config):
    manager = ChromeDriverManager(version='latest')
    browser = webdriver.Chrome(executable_path=manager.install())
    browser.maximize_window()
    browser.get(config['url'])
    yield browser
    browser.quit()
