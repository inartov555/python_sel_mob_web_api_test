"""
App config from ini config file
"""

from dataclasses import dataclass


@dataclass(slots=True)
class AppConfig:  # pylint: disable=too-many-instance-attributes
    """
    App config from ini config file
    """
    base_url: str
