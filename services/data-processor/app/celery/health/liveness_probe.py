from pathlib import Path

from celery import bootsteps

from app.constants import CeleryConfig


HEARTBEAT_FILE = Path(CeleryConfig.HEARTBEAT_FILE_PATH)


class LivenessProbe(bootsteps.StartStopStep):
    """
    Class for adding a scheduled task to worker.
    Creates a hearbeat file for the set interval.
    touch() creates or overwrites the hearbeat file with a new timestamp.
    Liveness can be probed by executing health_check_liveness.py.
    """

    requires = {"celery.worker.components:Timer"}

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.interval = 1.0
        self.tref = None

    def start(self, worker):
        """Hook up update_heartbeat_file() to event life cycle to create a hearbeat file by the given interval in seconds"""
        self.tref = worker.timer.call_repeatedly(
            self.interval,
            self.update_heartbeat_file,
            (worker,),
            priority=10,
        )

    def stop(self, worker):
        """Remove file on stop event"""
        HEARTBEAT_FILE.unlink(missing_ok=True)

    def update_heartbeat_file(self, worker):
        """Create a file for every heartbeat"""
        HEARTBEAT_FILE.touch()
