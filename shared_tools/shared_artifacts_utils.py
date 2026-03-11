"""
Web UI utils
"""

import os
from datetime import datetime

from shared_tools.logger.logger import Logger


class SharedArtifactsUtils:
    """
    Utils related to artifacts
    """


    @classmethod
    def timestamped_path(cls,
                         file_name: str,
                         file_ext: str,
                         host_artifacts: str = os.getenv("HOST_ARTIFACTS"),
                        ) -> str:
        """
        Args:
            file_name (str): e.g. screenshot
            file_ext (str): file extention, e.g., png
            host_artifacts (str): e.g. /home/user/test_dir/artifacts/

        Returns:
            str, timestamped path
        """
        ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S.%f")
        return os.path.join(host_artifacts, f"{file_name}-{ts}.{file_ext}")

    @classmethod
    def get_configured_logger(cls,
                              logger: Logger,
                              host_artifacts: str = os.getenv("HOST_ARTIFACTS"),
                              log_file_name: str = "pytest",
                              log_file_ext: str = "log",
                              log_level: str = "DEBUG",
                              log_file_level: str = "DEBUG",
                             ) -> Logger:
        """
        !!! Call it only in the main conftest.py to set logger.
        It uses built-in pytest arguments to configure loggigng level and files

        Parameters:
            log_level or --log-level general log level for capturing
            log_file_level or --log-file-level  level of log to be stored to a file. Usually lower than general log
            log_file or --log-file  path where logs will be saved
        """
        log_file = os.path.join(cls.timestamped_path(log_file_name, log_file_ext, host_artifacts))
        logger.setup_cli_handler(level=log_level)
        logger.setup_filehandler(level=log_file_level, file_name=log_file)
        logger.info(f"General loglevel: '{log_level}', File: '{log_file_level}'")
        return logger
