"""
Script for probing readiness of Celery workers.
Exits with non 0 status code if readiness file does not exists.
"""

import sys
from pathlib import Path

from app.constants import CeleryConfig

READINESS_FILE = Path(CeleryConfig.READIENES_FILE_PATH)

if not READINESS_FILE.is_file:
    sys.exit(1)

print("ok")
sys.exit(0)
