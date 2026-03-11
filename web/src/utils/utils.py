"""
Web UI utils
"""

import os

from selenium.webdriver.remote.webdriver import WebDriver

from shared_tools.shared_artifacts_utils import SharedArtifactsUtils


class ArtifactsUtils(SharedArtifactsUtils):
    """
    Utils related to artifacts
    """

    @classmethod
    def screenshot_dir(cls,
                       host_artifacts: str = os.getenv("HOST_ARTIFACTS"),
                      ) -> str:
        """
        Getting screenshot directory

        Args:
            host_artifacts (str): e.g. /home/user/test_dir/artifacts/
        """
        os.makedirs(host_artifacts, exist_ok=True)
        return host_artifacts

    @classmethod
    def take_screenshot(cls,
                        driver: WebDriver,
                        screenshot_name: str = "screenshot",
                        extension: str = "png",
                       ) -> None:
        """
        Take a screenshot
        """
        screenshot_path = cls.timestamped_path(screenshot_name, extension)
        driver.save_screenshot(screenshot_path)
