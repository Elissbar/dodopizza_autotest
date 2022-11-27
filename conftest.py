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
    """
    Фикстура, отвечающая за логирование тестов
    """
    log = logging.getLogger('test')

    path = os.path.join(test_dir, 'log_file.txt')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)-21s - %(lineno)d - %(message)s')
    file_handler = logging.FileHandler(path, 'w')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    log.addHandler(file_handler)
    log.setLevel(logging.DEBUG)
    log.propagate = False

    yield log

    for handler in log.handlers:
        handler.close()
        log.removeHandler(handler)
