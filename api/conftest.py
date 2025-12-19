"""
conftest.py file
"""
# pylint: disable=duplicate-code

import os
from datetime import datetime
from configparser import ConfigParser, ExtendedInterpolation

import pytest

from tools.logger.logger import Logger
from tools.url_utils import get_http_prot_url_port_separately
from api.api.public_api import PublicApi
from api.core.app_config import AppConfig


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
    # result_dict["base_url"] = cfg.get("pytest", "base_url", fallback="https://catfact.ninja")
    result_dict["base_url"] = cfg.get("pytest", "base_url", fallback="NONE")
    return AppConfig(**result_dict)


def pytest_addoption(parser):
    """
    Supported options
    """
    parser.addoption("--ini-config", action="store", default="pytest.ini", help="The path to the *.ini config file")


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


@pytest.fixture(autouse=True, scope="class")
def setup_api_testing(request):
    """
    Setting API instance for testing
    """
    _app_config = request.getfixturevalue("app_config")
    protocol, host, port = get_http_prot_url_port_separately(_app_config.base_url)
    request.cls.public_api = PublicApi(protocol, host, port)
