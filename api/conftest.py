"""
conftest.py file
"""

import os
from configparser import ConfigParser, ExtendedInterpolation

import pytest

from shared_tools.logger.logger import Logger
from shared_tools.url_utils import get_http_prot_url_port_separately
from shared_tools.shared_artifacts_utils import SharedArtifactsUtils
from api.api.public_api import PublicApi
from api.core.app_config import AppConfig


log = Logger(__name__)


# pylint: disable=duplicate-code
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
    log_file = os.path.join(SharedArtifactsUtils.timestamped_path("pytest", "log", artifacts_folder_default))
    log.setup_cli_handler(level=log_level)
    log.setup_filehandler(level=log_file_level, file_name=log_file)
    log.info(f"General loglevel: '{log_level}', File: '{log_file_level}'")
# pylint: enable=duplicate-code


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
    result_dict["base_url"] = cfg.get("pytest", "base_url", fallback="https://catfact.ninja")
    return AppConfig(**result_dict)


def pytest_addoption(parser) -> None:
    """
    Supported options
    """
    parser.addoption("--ini-config", action="store", default="pytest.ini", help="The path to the *.ini config file")


@pytest.fixture(autouse=True, scope="class")
def setup_api_testing(request) -> None:
    """
    Setting API instance for testing
    """
    _app_config = request.getfixturevalue("app_config")
    protocol, host, port = get_http_prot_url_port_separately(_app_config.base_url)[0:3]
    request.cls.public_api = PublicApi(protocol, host, port)
