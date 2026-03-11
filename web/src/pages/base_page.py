"""
Base methods for derived pages
"""

import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from shared_tools.logger.logger import Logger
from web.src.components.base_component import BaseComponent
from web.src.components.overlay_cookie_consent import CookieConsentOverlay
from web.src.components.overlay_transition_to_app import TransitionToAppOverlay


log = Logger(__name__)


class BasePage(BaseComponent):
    """
    Base methods for derived pages
    """

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.cookie_consent_overlay_comp = CookieConsentOverlay()
        self.transition_to_app_overlay_comp = TransitionToAppOverlay()

    def open(self, url: str = "") -> None:
        """
        Opening URL
        """
        self.driver.get(url)

    def scroll_by(self, x: int = 0, y: int = 700) -> None:
        """
        Scroll the page
        """
        self.driver.execute_script("window.scrollBy(arguments[0], arguments[1]);", x, y)

    def scroll_by_xy_repeat(self, x=0, y=700, times=1) -> None:
        """
        When you need to scroll particular number of times
        """
        for _ in range(times):
            self.scroll_by(x, y)
            self.pause(1)
        self.blur_active_element()

    def scroll_into_center(self, locator) -> None:
        """
        Scroll into center
        """
        web_element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", web_element)

    def tap_empty_space(self) -> None:
        """
        Tapping empty space
        """
        try:
            self.action_chains().move_by_offset(1, 1).click().perform()
        except Exception:
            pass

    def focus_first_visible(self, locator) -> None:
        """
        Returns:
            WebElement, focused element
        """
        try:
            web_element = self.find_first_visible_in_viewport(locator)
            self.driver.execute_script("arguments[0].focus();", web_element)
            return web_element
        except Exception as ex:
            log.error(f"Failed to focus visible element: {ex}")
        return None

    def find_first_visible_in_viewport(self,
                                       locator,
                                       min_ratio: float = 0.5,
                                       top_margin: int = 90,
                                       bottom_margin: int = 0) -> WebElement:
        """
        Get the 1st visible element which is visible at list by min_ratio in view port and not covered by other elements.

        Returns:
            WebElement
        """
        by, value = locator

        if by == By.CSS_SELECTOR:
            js = """
            const sel = arguments[0], ratio = arguments[1], topM = arguments[2], bottomM = arguments[3];
            const vh = window.innerHeight || document.documentElement.clientHeight;
            const els = Array.from(document.querySelectorAll(sel));
            function visible(el){
              const r = el.getBoundingClientRect();
              const styles = window.getComputedStyle(el);
              if (styles.display === 'none' || styles.visibility === 'hidden' || parseFloat(styles.opacity) === 0) return false;

              const top    = Math.max(r.top, topM);
              const bottom = Math.min(r.bottom, vh - bottomM);
              const visH   = Math.max(0, bottom - top);
              const height = Math.max(1, r.height);

              if (visH/height < ratio) return false;

              // перевірка перекриття: беремо точку в центрі видимої частини
              const x = Math.floor(r.left + r.width/2);
              const y = Math.floor(top + Math.min(visH, height)/2);
              const e = document.elementFromPoint(x, y);
              return e && (el === e || el.contains(e));
            }
            return els.find(visible) || null;
            """
            return self.driver.execute_script(js, value, float(min_ratio), int(top_margin), int(bottom_margin))
        if by == By.XPATH:
            js = """
            const xpath = arguments[0], ratio = arguments[1], topM = arguments[2], bottomM = arguments[3];
            const vh = window.innerHeight || document.documentElement.clientHeight;
            const snap = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
            const els = [];
            for (let i = 0; i < snap.snapshotLength; i++) els.push(snap.snapshotItem(i));

            function visible(el){
              const r = el.getBoundingClientRect();
              const styles = window.getComputedStyle(el);
              if (styles.display === 'none' || styles.visibility === 'hidden' || parseFloat(styles.opacity) === 0) return false;

              const top    = Math.max(r.top, topM);
              const bottom = Math.min(r.bottom, vh - bottomM);
              const visH   = Math.max(0, bottom - top);
              const height = Math.max(1, r.height);

              if (visH/height < ratio) return false;

              const x = Math.floor(r.left + r.width/2);
              const y = Math.floor(top + Math.min(visH, height)/2);
              const e = document.elementFromPoint(x, y);
              return e && (el === e || el.contains(e));
            }
            return els.find(visible) || null;
            """
            return self.driver.execute_script(js, value, float(min_ratio), int(top_margin), int(bottom_margin))
        raise ValueError("Use CSS_SELECTOR or XPATH for this helper.")

    def confirm_cookies_overlay_if_shown(self) -> None:
        """
        Clicking the Accept button on the "Cookies and Advertising Choices" overlay, if it's shown
        """
        self.cookie_consent_overlay_comp.confirm_cookies_overlay_if_shown(raise_error_if_not_visible=False)

    def get_out_of_transition_to_app_overlay(self) -> None:
        """
        Clicking the Accept button on the "Cookies and Advertising Choices" overlay, if it's shown
        """
        self.transition_to_app_overlay_comp.get_out_of_transition_to_app_overlay(raise_error_if_not_visible=False)
