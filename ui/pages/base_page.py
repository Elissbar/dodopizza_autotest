from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ES


CLICK_RETRY = 3


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def wait(self, timeout=10):
        return WebDriverWait(self.driver, timeout)

    def find_element(self, locator, timeout=10):
        return self.wait(timeout).until(ES.presence_of_element_located(locator))

    def find_child_element(self, parent_element, child_locator):
        # parent_element = self.find_element(parent_locator)
        return WebDriverWait(parent_element, 5).until(ES.presence_of_element_located(child_locator))
        # return self.find_element(parent_locator)

    def find_elements(self, locator, timeout=10):
        return self.wait(timeout).until(ES.presence_of_all_elements_located(locator))

    def move_to_element(self, element):
        action = ActionChains(self.driver)
        return action.move_to_element(element).perform()

    def click_and_hold(self, element):
        action = ActionChains(self.driver)
        return action.click_and_hold(element).pause(5).perform()

    def is_clickable(self, locator):
        return self.wait().until(ES.element_to_be_clickable(locator))
        # return self.wait().until(ES.visibility_of_element_located(locator))

    def click(self, locator):
        for i in range(CLICK_RETRY):
            try:
                self.find_element(locator)
                elem = self.is_clickable(locator)
                self.move_to_element(elem)
                elem.click()
                return
            except:
                if i == CLICK_RETRY-1:
                    raise




