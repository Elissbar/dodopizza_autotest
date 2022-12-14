from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ES
from selenium.common.exceptions import TimeoutException
import logging


CLICK_RETRY = 3


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger('test')

    def wait(self, timeout=15):
        return WebDriverWait(self.driver, timeout)

    def find_element(self, locator, timeout=15):
        try:
            elem = self.wait(timeout).until(ES.presence_of_element_located(locator))
            self.logger.debug(f'Поиск элемента: {locator[1]}')
            return elem
        except TimeoutException:
            self.logger.debug(f'Элемент не найден: {locator[1]}')
            raise TimeoutException

    def find_elements(self, locator, timeout=15):
        self.logger.debug(f'Поиск множества элементов: {locator[1]}')
        return self.wait(timeout).until(ES.presence_of_all_elements_located(locator))

    def find_child_element(self, parent_element, child_locator):
        self.logger.debug(f'Поиск дочернего элемента: {child_locator[1]}')
        return WebDriverWait(parent_element, 15).until(ES.presence_of_element_located(child_locator))

    def move_to_element(self, element):
        action = ActionChains(self.driver)
        return action.move_to_element(element).perform()

    def click(self, locator=None):
        for i in range(CLICK_RETRY):
            try:
                self.find_element(locator)
                elem = self.wait().until(ES.element_to_be_clickable(locator))
                self.move_to_element(elem)
                self.logger.debug(f'Клик на элемент: {locator[1]}')
                elem.click()
                return
            except:
                self.logger.debug(f'Не удалось нажать на элемент: {locator[1]}')
                if i == CLICK_RETRY-1:
                    raise
