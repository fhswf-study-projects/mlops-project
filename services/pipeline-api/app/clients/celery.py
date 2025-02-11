import os
from celery import Celery

from app.constants import EnvConfig


class CeleryClient:
    _instance = None

    def __new__(cls):
        """Returns the singleton instance or creates a new one if not existend"""
        if cls._instance is None:
            cls._instance = super(CeleryClient, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self._app = Celery(
            "gate",
            broker=os.environ[EnvConfig.CELERY_BROKER_CONNECTION.value],
            backend=os.environ[EnvConfig.CELERY_BACKEND_CONNECTION.value],
        )
        self._app.conf.update(
            result_extended=True,
            worker_send_task_events=True,
            task_send_sent_event=True,
        )

    def get_app(self) -> Celery:
        return self._app
