"""
Script for probing liveness of Celery workers.
Exits with non 0 status code if hearbeat file does not exist exist or is older then 60 seconds.
"""

import sys
import time
from pathlib import Path


from app.constants import CeleryConfig
from loguru import logger


HEARTBEAT_FILE = Path(CeleryConfig.HEARTBEAT_FILE_PATH)

if not HEARTBEAT_FILE.is_file():
    logger.error("Celery liveness file not found")
    sys.exit(1)

time_diff = time.time() - HEARTBEAT_FILE.stat().st_mtime

if time_diff > 60:
    logger.error("Celery liveness file does not fulfil constraints")
    sys.exit(1)

sys.exit(0)
