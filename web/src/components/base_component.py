"""
Base class for components
"""

from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BaseComponent:
    """
    Base class for components
    """
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def open(self, url: str = "") -> None:
        """
        Opening URL
        """
        self.driver.get(url)

    def action_chains(self) -> ActionChains:
        """
        Get ActionChains instance
        """
        return ActionChains(self.driver)

    def web_driver_wait(self, timeout: int = 5) -> WebDriverWait:
        """
        Setting WebDriverWait
        """
        return WebDriverWait(self.driver, timeout)

    def click_and_drag(self, locator, move_by_x: int = 0, move_by_y: int = 300) -> None:
        """
        Clicking and dragging an element
        """
        web_element = self.driver.find_element(*locator)
        self.action_chains().click_and_hold(web_element).move_by_offset(move_by_x, move_by_y).release().perform()

    def blur_active_element(self) -> None:
        """
        Unfocusing the element being focused
        """
        self.driver.execute_script("document.activeElement && document.activeElement.blur();")

    def is_displayed(self, locator) -> bool:
        """
        Check if element is displayed
        """
        try:
            result = self.driver.find_element(*locator).is_displayed()
        except (NoSuchElementException, StaleElementReferenceException):
            result = False
        return result

    def wait_visible(self, locator, timeout: int = 5) -> bool:
        """
        Wait visible
        """
        return self.web_driver_wait(timeout).until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator, timeout: int = 5) -> bool:
        """
        Wait clickable
        """
        return self.web_driver_wait(timeout).until(EC.element_to_be_clickable(locator))

    def click(self, locator) -> None:
        """
        Regular click
        """
        self.wait_clickable(locator).click()

    def js_click(self, locator) -> None:
        """
        JavaScript click
        """
        web_element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].click();", web_element)

    def type_text(self, locator, text: str) -> None:
        """
        Type text
        """
        el = self.wait_visible(locator)
        el.clear()
        el.send_keys(text)

    def maybe_click(self, locator) -> bool:
        """
        Tries to click, no effect if element is not clickable
        """
        try:
            self.click(locator)
            return True
        except (
            TimeoutException,
            ElementClickInterceptedException,
            StaleElementReferenceException,
        ):
            return False
