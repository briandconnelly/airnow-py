# -*- coding: utf-8 -*-

import logging
import os


logger = logging.getLogger("airnow")
logging.basicConfig(
    format="-- [%(asctime)s][%(levelname)s][%(name)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

__DEBUG__ = os.environ.get("AIRNOW_DEBUG", False)

if __DEBUG__:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
