import shutil
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
import json
import logging


root_dir = os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='session')
def config():
    data = open(os.path.join(root_dir, 'data.json'), 'r')
    data = json.loads(data.read())
    for key, value in data.items():
        try:
            data[key] = int(value)
        except:
            data[key] = value
    return data


def pytest_configure(config):
    path = os.path.join(root_dir, 'artifacts')
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    config.artifacts = path


@pytest.fixture(scope='function')
def driver(config):
    manager = ChromeDriverManager(version='latest')
    browser = webdriver.Chrome(executable_path=manager.install())
    browser.maximize_window()
    browser.get(config['url'])
    yield browser
    browser.quit()


@pytest.fixture(scope='function')
def test_dir(request, config):
    test_name = request.node.nodeid.replace(':', '_')
    test_dir_name = os.path.join(request.config.artifacts, test_name)
    os.makedirs(test_dir_name)
    return test_dir_name


@pytest.fixture(scope='function', autouse=True)
def make_screenshot(config, driver, test_dir):
    yield
    path_screenshot = os.path.join(test_dir, 'screenshot.png')
    driver.save_screenshot(path_screenshot)


@pytest.fixture(scope='function')
def logger(config, test_dir):
    logger = logging.getLogger('test')

    path = os.path.join(test_dir, 'log_file.txt')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(path, 'w')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    return logger




