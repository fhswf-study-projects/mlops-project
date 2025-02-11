import os
import inspect
import pkgutil
import importlib
from pathlib import Path

from loguru import logger

from celery import Task
from celery import Celery
from celery.signals import worker_ready, worker_shutdown

from app.constants import EnvConfig, CeleryConfig
from app.celery.health.liveness_probe import LivenessProbe

READINESS_FILE = Path(CeleryConfig.READIENES_FILE_PATH)


@worker_ready.connect
def worker_ready(**_):
    """Creates a readiness file when worker is ready"""
    READINESS_FILE.touch()


@worker_shutdown.connect
def worker_shutdown(**_):
    """Remove Rreadiness file when worker is shutting down"""
    READINESS_FILE.unlink(missing_ok=True)


logger.info("Setup Celery App")

app = Celery(
    "gate",
    broker=os.environ[EnvConfig.CELERY_BROKER_CONNECTION.value],
    backend=os.environ[EnvConfig.CELERY_BACKEND_CONNECTION.value],
)

app.conf.update(
    task_default_queue=os.environ[EnvConfig.CELERY_DEFAULT_QUEUE.value],
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    broker_pool_limit=None,
    result_extended=True,
    worker_send_task_events=True,
    task_send_sent_event=True,
)

app.steps["worker"].add(LivenessProbe)

tasks = []

for x in pkgutil.iter_modules(["app/tasks"]):
    # import the module and iterate through its attributes
    module = importlib.import_module(f"app.tasks.{x.name}")
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)

        if inspect.isclass(attribute) and issubclass(attribute, Task):
            try:
                tasks.append(attribute())
            except Exception as e:
                logger.exception(f"Couldn't instantiate {attribute_name}: {str(e)}")

for task in tasks:
    app.register_task(task)
