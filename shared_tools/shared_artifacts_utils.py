"""
Web UI utils
"""

import os
from datetime import datetime


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
