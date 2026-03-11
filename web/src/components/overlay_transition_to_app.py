"""
Transition to app overlay component
"""

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from web.src.components.base_component import BaseComponent


class TransitionToAppOverlay(BaseComponent):
    """
    Transition to app overlay component
    """
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        # Sometimes, transition to app overlay is shown when selecting, e.g., the search button,
        # this overlay consists of 2 parts
        self.transition_to_app_overlay = (By.XPATH,
            "//div[@class='ScReactModalBase-sc-26ijes-0 foAhuv tw-modal-layer']//div[@class='Layout-sc-1xcs6mc-0 cBrePX']")
        self.close_overlay = (By.XPATH,
            "//div[@class='ScReactModalBase-sc-26ijes-0 foAhuv tw-modal-layer']"
            "//button[@class='InjectLayout-sc-1i43xsx-0 ccdBQN']"
        )

    def handle_transition_to_app_overlay(self, raise_error_if_not_visible: bool = False) -> None:
        """
        Clicking the Accept button on the "Cookies and Advertising Choices" overlay
        """
        try:
            if self.wait_visible(self.transition_to_app_overlay, 2):
                self.js_click(self.close_overlay)
        except TimeoutException:
            if raise_error_if_not_visible:
                raise
