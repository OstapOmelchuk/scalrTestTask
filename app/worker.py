import threading
import queue
import time

import database
import typing

import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


LOG = logging.getLogger(__name__)

class Worker:
    def __init__(self, num_of_workers=1):
        self.queue = queue.Queue()
        self.num_of_workers = num_of_workers

    def start_workers(self):
        LOG.debug("Starting %s workers.", self.num_of_workers)
        for i in range(self.num_of_workers):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()

    def worker(self):
        while True:
            item = self.queue.get()
            self._process_task(item)
            self.queue.task_done()

    def wait(self):
        """Wait for all tasks to be processed."""
        self.queue.join()

    def _put_task(self, task: database.Task):
        self.queue.put(task)

    def _process_task(self, task: database.Task):
        LOG.debug("Processing task %s.", task)
        raise NotImplementedError

    def _gather_tasks(self) -> typing.Sequence[database.Task]:
        """Gather all tasks.py in the database."""
        raise NotImplementedError

    def start(self):
        database.init_database()
        self.start_workers()

        while True:
            tasks = self._gather_tasks()
            if tasks:
                for task in tasks:
                    self._put_task(task)
            else:
                LOG.debug("No tasks found, sleeping for 1 seconds.")
                time.sleep(1)

            self.wait()


w = Worker()
w.start()
