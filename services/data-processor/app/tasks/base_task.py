import celery


class BaseTask(celery.Task):
    name = "base_task"

    def run(self, data, **kwargs):
        return {"result": "ok"}
