from pathlib import Path

from celery import Celery
from celery.signals import after_task_publish

from WebDownloader.core.config import Config
from WebDownloader.jobs.tasks import ImageTask, TextTask


class CeleryServer(Celery):

    textTask: TextTask

    imageTask: ImageTask

    def __init__(self, config: Config, **kwargs):
        self.config = config
        super().__init__(__name__, broker=self.config['BROKER_URL'], backend=self.config['CELERY_RESULT_BACKEND'], **kwargs)
        self.textTask = self.register_task(TextTask(config))
        self.imageTask = self.register_task(ImageTask(config))


    def check_state(self, task_id: str):
        """Checks task's state
        Because all tasks are PENDING by default, it's replaced with SENT,
        (PENDING means NOT FOUND)

        :param task_id: task's id
        :return: task's status
        """
        status = self.AsyncResult(task_id).status
        if status == 'PENDING':
            status = 'NOT FOUND'
        return status

    def find_result(config: Config, task_id: str) -> str:
        """Specifies name of result file

        :param task_id: task's id
        :return: name of result file
        """
        db = config.opt['DATA_LOCATION']
        file_path = db.joinpath(Path(task_id))
        if file_path.with_suffix('.txt').exists():
            return task_id + '.txt'
        elif file_path.with_suffix('.zip').exists():
            return task_id + '.zip'
        else:
            raise FileNotFoundError('Result file not found')

    @after_task_publish.connect
    def update_sent_state(self, sender=None, headers=None, **kwargs):
        """
            Updates task when it's sent to mark it is created
            (because celery by default does not distinguish pending and not existing tasks)
        """
        task = self.tasks.get(sender)
        backend = task.backend if task else CeleryServer.backend
        backend.store_result(headers['id'], None, "SENT")




