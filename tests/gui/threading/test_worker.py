import pytest
from PySide6.QtTest import QSignalSpy

from stegos.gui.threading.worker import Worker


def _mock_error():
    """Mock error function."""
    raise ValueError


def _mock_generator():
    """Mock generator function."""
    yield 1
    yield 2


class TestWorker:
    """Tests for Worker."""

    @pytest.mark.parametrize(
        ("func", "result_count", "error_count"),
        [(lambda: 1, 1, 0), (_mock_generator, 2, 0), (_mock_error, 0, 1)],
    )
    def test_signals(self, qtbot, func, result_count, error_count):
        """Signals should be emitted to communicate state (started, finished, result, and error)."""
        worker = Worker(func)

        started_spy = QSignalSpy(worker.signals.started)
        result_spy = QSignalSpy(worker.signals.result)
        error_spy = QSignalSpy(worker.signals.error)
        finished_spy = QSignalSpy(worker.signals.finished)

        worker.run()

        assert started_spy.count() == 1
        assert result_spy.count() == result_count
        assert error_spy.count() == error_count
        assert finished_spy.count() == 1
