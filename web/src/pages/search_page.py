"""
Search page
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

from shared_tools.logger.logger import Logger
from web.src.pages.base_page import BasePage


log = Logger(__name__)


class SearchPage(BasePage):
    """
    Search page
    """
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.search_input = (By.CSS_SELECTOR, "input[type='search'], input[aria-label='Search']")
        self.first_result = (
            By.XPATH,
            "//section//a[starts-with(@href, '/videos/')] | "
            "//section//button[@class='ScCoreLink-sc-16kq0mq-0 cZfgmJ InjectLayout-sc-1i43xsx-0 ggvZjN tw-link']")

    def type_text_and_press_enter(self, input_text: str) -> None:
        """
        Typing search text, starting search and the unfocusing active element
        """
        log.info("Type text and press enter")
        self.type_text(self.search_input, input_text + Keys.ENTER)
        self.blur_active_element()

    def open_first_streamer(self) -> None:
        """
        Heuristic: click the first visible result anchor
        """
        log.info("Select the first video in the visible list")
        self.wait_visible(self.first_result)
        el = self.focus_first_visible(self.first_result)
        el.click()
