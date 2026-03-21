from PySide6.QtCore import QThreadPool

from stegos.gui.model.concurrency import Worker


class WorkerExecutor:
    """Executor for workers."""

    @staticmethod
    def run(func, *args, **kwargs) -> Worker:
        """
        Runs a function in a seperate thread.

        The execution of the function is queued if the global thread pool is full.
        :param func: Function to execute in a seperate thread.
        :param args: Arguments for the function.
        :param kwargs: Keyword arguments for the function.
        :return: Worker that runs in a seperate thread.
        """
        worker = Worker(func, *args, **kwargs)
        QThreadPool.globalInstance().start(worker)
        return worker
