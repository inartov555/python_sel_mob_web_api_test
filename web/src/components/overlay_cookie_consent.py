"""
Cookie consent overlay component
"""

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from web.src.components.base_component import BaseComponent


class CookieConsentOverlay(BaseComponent):
    """
    Cookie consent overlay component
    """
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.accept_button = (By.XPATH, "//button[@data-a-target='consent-banner-accept']")

    def handle_cookies_overlay(self, raise_error_if_not_visible: bool = False) -> None:
        """
        Clicking the Accept button on the "Cookies and Advertising Choices" overlay
        """
        try:
            self.wait_visible(self.accept_button)
            self.click(self.accept_button)
        except TimeoutException:
            if raise_error_if_not_visible:
                raise
