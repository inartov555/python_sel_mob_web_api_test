"""
Twitch mobile tests
"""

import pytest

from shared_tools.logger.logger import Logger
from web.conftest import timestamped_path
from web.src.utils import ArtifactsUtils


log = Logger(__name__)


@pytest.mark.mobile
class TestTwitchMobile:
    """
    Twitch mobile tests
    """

    def test_search_and_open_streamer(self, base_url) -> None:
        """
        Search and open streamer
        """
        # 1. Open home
        self.home_page.open(base_url)
        # 2. Tap search icon
        self.home_page.open_search()
        # 3. Type query
        self.search_page.type_text_and_press_enter("StarCraft II")
        # 4. Scroll down twice (small delays to simulate user)
        self.search_page.scroll_by_xy_repeat(times=2)
        # 5. Open a streamer
        self.search_page.open_first_streamer()
        # 6. Wait for streamer page to load; take screenshot
        self.streamer_page.ensure_loaded()
        # 7. Taking a screenshot
        ArtifactsUtils.take_screenshot("test_search_and_open_streamer", "png")
        log.debug(f"Saved screenshot: {screenshot_path}")
