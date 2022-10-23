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
    """
    Сбор тестовых данных из файла data.json
    :return: dict - тестовые данные
    """
    data = open(os.path.join(root_dir, 'data.json'), 'r', encoding='utf-8')
    data = json.loads(data.read())
    for key, value in data.items():
        try:
            data[key] = int(value)
        except:
            data[key] = value
    return data


def pytest_configure(config):
    """
    Создание папки artifacts для хранения логов и скриншотов тестов
    :param config:
    :return:
    """
    path = os.path.join(root_dir, 'artifacts')
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    config.artifacts = path


@pytest.fixture(scope='function')
def driver(config, logger):
    """
    Инициализация браузера и открытие страницы
    """
    options = webdriver.ChromeOptions()
    manager = ChromeDriverManager(version='latest')
    browser = webdriver.Chrome(executable_path=manager.install(), chrome_options=options)
    browser.maximize_window()
    logger.debug(f'Переход на страницу: {config["url"]}')
    browser.get(config['url'])
    yield browser
    browser.quit()


@pytest.fixture(scope='function')
def test_dir(request):
    test_name = request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_')
    test_dir = os.path.join(request.config.artifacts, test_name)
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='function', autouse=True)
def make_screenshot(config, driver, test_dir):
    """
    Фикстура, которая делает скриншот по окончанию тестов
    """
    yield
    path_screenshot = os.path.join(test_dir, 'screenshot.png')
    driver.save_screenshot(path_screenshot)


@pytest.fixture(scope='function')
def logger(config, test_dir):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)-s - %10(levelname)-s: %(message)s')
    log_file = os.path.join(test_dir, 'test.log')

    # log_level = logging.DEBUG if config['debug_log'] else logging.INFO
    log_level = logging.DEBUG

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()



