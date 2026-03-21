from typing import Generator

from PySide6.QtCore import QObject, Signal, QRunnable, Slot


class WorkerSignals(QObject):
    """Signals for Worker.

    As Worker is NOT a subclass of QObject, it can not hold signals. Therefore, this class is necessary for adding signals to Workers.
    """

    started = Signal()
    result = Signal(object)
    error = Signal(Exception)
    finished = Signal()


class Worker(QRunnable):
    """Allows functions to be run in a seperate thread.

    Supports regular and generator functions.
    """

    def __init__(self, func, *args, **kwargs):
        """
        Creates an instance of Worker.
        :param func: Function to run in a seperate thread.
        :param args: Arguments for the function.
        :param kwargs: Keyword arguments for the function.
        """
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        """Runs the function in a seperate thread. Should only be used by thread pools."""
        self.signals.started.emit()
        try:
            result = self.func(*self.args, **self.kwargs)
            if isinstance(result, Generator):
                for value in result:
                    self.signals.result.emit(value)
            else:
                self.signals.result.emit(result)
        except Exception as e:
            self.signals.error.emit(e)
        finally:
            self.signals.finished.emit()
