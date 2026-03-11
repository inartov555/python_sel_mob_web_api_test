"""
Home page
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from shared_tools.logger.logger import Logger
from web.src.pages.base_page import BasePage


log = Logger(__name__)


class HomePage(BasePage):
    """
    Home page
    """
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.search_icon = (By.XPATH, "//a[@href='/directory']/div/div")

    def open_search(self) -> None:
        """
        Open search page
        """
        self.click(self.search_icon)
        self.get_out_of_transition_to_app_overlay()  # sometimes, app transition overlay is shown at this point
