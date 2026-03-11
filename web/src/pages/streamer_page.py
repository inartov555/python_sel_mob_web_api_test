"""
Streamer page
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from shared_tools.logger.logger import Logger
from web.src.pages.base_page import BasePage


log = Logger(__name__)


class StreamerPage(BasePage):
    """
    Streamer page
    """
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        # Possible popups (consent, mature content, cookie, login prompts, etc.)
        self.dismiss_selectors = [
            (By.CSS_SELECTOR, "button[aria-label='Close'], button[aria-label='Dismiss']"),
            (By.CSS_SELECTOR, "button:has(svg[aria-label='Close'])"),
            (By.CSS_SELECTOR, "button[data-a-target='consent-banner-accept'], button[aria-label*='Accept']"),
            (By.XPATH, "//button[contains(normalize-space(.), 'Continue')] | //a[contains(normalize-space(.), 'Continue')]")
        ]
        self.video_player = (By.CSS_SELECTOR, "video, div[data-a-target='video-player'], div[class*='player']")
        self.channel_header = (By.CSS_SELECTOR, "header, h1, h2")

    def ensure_loaded(self) -> bool:
        """
        Make sure the video/player is visible
        """
        # Try to close any modal/popups if they appear
        for loc in self.dismiss_selectors:
            self.maybe_click(loc)
        try:
            return self.wait_visible(self.video_player)
        except Exception:
            return self.wait_visible(self.channel_header)
