import logging
import random
from queue import Queue
from threading import Thread
from time import sleep

from sqlalchemy.orm import Session

from app.config import AppConfig, get_config
from app.schemas import Task

config = get_config()


# FIXME: threading is not recommended in FastAPI, use Celery instead
class Worker:
    def __init__(self, config: AppConfig, db: Session):
        self.config = config
        self.db = db
        self.run_flag = True
        self.task_queue: Queue[Task] = Queue()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(config.LOG_LEVEL.value)
        self.log_handler = logging.StreamHandler()
        self.log_handler.setLevel(config.LOG_LEVEL.value)
        self.log_formatter = logging.Formatter(config.LOG_FORMAT)
        self.log_handler.setFormatter(self.log_formatter)
        self.logger.addHandler(self.log_handler)
        self.logger.debug("Worker initialized")
        self._thread = Thread(target=self._run)
        self._thread.start()

    def _run(self):
        # Perform your background work here
        sleep_interval = 0
        while self.run_flag:
            if not self.task_queue.empty():
                self.logger.debug(f"Task queue size: {self.task_queue.qsize()}")
                task = self.task_queue.get(timeout=1)
                self.logger.info(f"Processing task {task.id}")
                # Do something with the task
                sleep(1)
                self.logger.info(f"Task {task.id} processed")
                # Reset sleep interval
                sleep_interval = 0
            else:
                # No task, exponential backoff with jitter
                self.logger.info(f"No task, sleeping for {2**sleep_interval} seconds")
                micro_sleep = 0.1 * random.random()
                acc_sleep = 0
                while (acc_sleep < 2**sleep_interval) and self.run_flag:
                    sleep(micro_sleep)
                    acc_sleep += micro_sleep
                    micro_sleep = 0.1 * random.random()
                if sleep_interval < 10:
                    sleep_interval += 1

    def add_task(self, task: Task):
        # Add a task to the queue
        self.logger.info(f"Adding task {task.id} to the queue")
        self.task_queue.put(task)

    def shutdown(self):
        # Perform any cleanup operations
        self.run_flag = False

    def start(self):
        # Perform any initialization operations
        self.run_flag = True
        self._thread = Thread(target=self._run)
        self._thread.start()
