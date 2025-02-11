import celery


class TestTask(celery.Task):
    name = "test"

    def run(self, data, **kwargs):
        return {"result": 2+2}
