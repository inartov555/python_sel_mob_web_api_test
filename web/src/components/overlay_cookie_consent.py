"""
Cookie consent overlay component
"""

from selenium.common.exceptions import TimeoutException


class CookieConsentOverlay:
    """
    Cookie consent overlay component
    """
    def __init__(self) -> None:
        self.accept_button = (By.XPATH, "//button[@data-a-target='consent-banner-accept']")

    def confirm_cookies_overlay_if_shown(self, raise_error_if_not_visible: bool = False) -> None
        """
        Clicking the Accept button on the "Cookies and Advertising Choices" overlay
        """
        try:
            self.wait_visible(self.accept_button)
            self.click(self.accept_button)
        except TimeoutException:
            if raise_error_if_not_visible:
                raise
