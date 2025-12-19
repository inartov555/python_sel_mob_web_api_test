"""
conftest.py file
"""
# pylint: disable=duplicate-code

import os
from datetime import datetime
from configparser import ConfigParser, ExtendedInterpolation

import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

from tools.logger.logger import Logger
from web.src.pages.home_page import HomePage
from web.src.pages.search_page import SearchPage
from web.src.pages.streamer_page import StreamerPage
from web.src.core.app_config import AppConfig


log = Logger(__name__)


@pytest.fixture(autouse=True, scope="session")
def add_loggers() -> None:
    """
    The fixture to configure loggers
    It uses built-in pytest arguments to configure loggigng level and files

    Parameters:
        log_level or --log-level general log level for capturing
        log_file_level or --log-file-level  level of log to be stored to a file. Usually lower than general log
        log_file or --log-file  path where logs will be saved
    """
    artifacts_folder_default = os.getenv("HOST_ARTIFACTS")
    log_level = "DEBUG"
    log_file_level = "DEBUG"
    log_file = os.path.join(timestamped_path("pytest", "log", artifacts_folder_default))
    log.setup_cli_handler(level=log_level)
    log.setup_filehandler(level=log_file_level, file_name=log_file)
    log.info(f"General loglevel: '{log_level}', File: '{log_file_level}'")


@pytest.fixture(scope="session")
def app_config(pytestconfig) -> AppConfig:
    """
    Set and get AppConfig from ini config
    """
    ini_config_file = pytestconfig.getoption("--ini-config")
    log.info(f"Reading config properties from '{ini_config_file}' and storing to a data class")
    result_dict = {}
    cfg = ConfigParser(interpolation=ExtendedInterpolation())
    cfg.read(ini_config_file)
    result_dict["browser"] = cfg.get("pytest", "browser", fallback="chrome")
    result_dict["device"] = cfg.get("pytest", "device", fallback="Pixel 5")
    result_dict["base_url"] = cfg.get("pytest", "base_url", fallback="https://m.twitch.tv")
    result_dict["is_headless"] = cfg.getboolean("pytest", "is_headless", fallback=False)
    result_dict["width"] = cfg.getint("pytest", "width", fallback=400)
    result_dict["height"] = cfg.getint("pytest", "height", fallback=1000)
    return AppConfig(**result_dict)


def pytest_addoption(parser):
    """
    Supported options
    """
    parser.addoption("--ini-config", action="store", default="pytest.ini", help="The path to the *.ini config file")


@pytest.fixture(scope="session")
def screenshot_dir() -> str:
    """
    Getting screenshot directory
    """
    # path_from_input_params = pytestconfig.getoption("--screenshot-dir")
    artifacts_folder_default = os.getenv("HOST_ARTIFACTS")
    os.makedirs(artifacts_folder_default, exist_ok=True)
    return artifacts_folder_default


def timestamped_path(file_name: str, file_ext: str, path_to_file: str = os.getenv("HOST_ARTIFACTS")) -> str:
    """
    Args:
        file_name (str): e.g. screenshot
        file_ext (str): file extention, e.g., png
        path_to_file (str): e.g. /home/user/test_dir/artifacts/

    Returns:
        str, timestamped path
    """
    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S.%f")
    return os.path.join(path_to_file, f"{file_name}-{ts}.{file_ext}")


def get_driver(browser: str, pytestconfig, request) -> WebDriver:
    """
    Get a driver for passed browser settings
    """
    _app_config = request.getfixturevalue("app_config")
    if browser in ("chrome", "chromium"):
        window_size = pytestconfig.getoption("--window-size", f"{_app_config.width},{_app_config.height}")
        headless = _app_config.is_headless

        options = Options()
        mobile_emulation = get_mobile_emulation(_app_config.device)
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--window-size={window_size}")

        _driver = webdriver.Chrome(options=options)
        _driver.set_page_load_timeout(60)
        return _driver
    else:
        raise ValueError(f"'{browser}' value is not currently supported")


@pytest.fixture(scope="session")
def driver(pytestconfig, request):
    """
    Browser driver
    """
    _app_config = request.getfixturevalue("app_config")
    _driver = get_driver(_app_config.browser, pytestconfig, request)
    yield _driver
    _driver.quit()


# pylint: disable=redefined-outer-name
@pytest.fixture(autouse=True, scope="function")
def setup_for_testing(request, driver):
    """
    Setting up pages for testing
    """
    request.cls.driver = driver
    request.cls.home_page = HomePage(driver)
    request.cls.search_page = SearchPage(driver)
    request.cls.streamer_page = StreamerPage(driver)

    # 1. Open home
    request.cls.home_page.open("https://m.twitch.tv")
    # Getting rid off the cookies overlay
    request.cls.home_page.confirm_cookies_overlay_if_shown()


def get_mobile_emulation(version):
    """
    If you get "selenium.common.exceptions.InvalidArgumentException: Message:
    invalid argument: cannot parse capability: goog:chromeOptions" error,
    you need to provide capability manually
    """
    mobile_emulation = {"deviceName": version}
    if version == "Pixel 5":
        mobile_emulation = {
        "deviceMetrics": {
            "width": 393,    # width for Pixel 5 (dp)
            "height": 851,   # height for Pixel 5 (dp)
            "pixelRatio": 2.75
        },
        "userAgent": (
            "Mozilla/5.0 (Linux; Android 11; Pixel 5) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Mobile Safari/537.36"
        )
    }
    return mobile_emulation
