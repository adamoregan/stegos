import pytest
from PySide6.QtCore import QMimeData, QUrl, QPoint, Qt
from PySide6.QtGui import QDropEvent
from PySide6.QtTest import QSignalSpy
from PySide6.QtWidgets import QWidget

from stegos.gui.controller.filesystem import FileSystemDropHandler


def create_mime_files(paths: list[str]) -> QMimeData:
    mime = QMimeData()
    mime.setUrls([QUrl.fromLocalFile(p) for p in paths])
    return mime


def create_mime_text(text: str) -> QMimeData:
    mime = QMimeData()
    mime.setText(text)
    return mime


def create_mime_urls(urls: list[str]) -> QMimeData:
    mime = QMimeData()
    mime.setUrls([QUrl(u) for u in urls])
    return mime


class TestFileSystemDropHandler:
    """Tests for FileSystemDropHandler"""

    @pytest.mark.parametrize(
        ("mime", "expected_payload"),
        [
            (create_mime_text("hello"), None),
            # url edgecase, since local files are treated like urls (e.g. file://)
            (create_mime_urls(["https://example.com"]), None),
            (create_mime_files(["/tmp/file.txt"]), ["/tmp/file.txt"]),
        ],
    )
    def test_itemsDropped(self, qtbot, mime, expected_payload):
        """A signal should be emitted when valid filesystem items are dropped."""
        widget = QWidget()
        qtbot.addWidget(widget)
        handler = FileSystemDropHandler(widget)

        event = QDropEvent(
            QPoint(0, 0),
            Qt.DropAction.CopyAction,
            mime,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
        )

        spy = QSignalSpy(handler.itemsDropped)
        handler.eventFilter(widget, event)
        if expected_payload:
            assert spy.at(0)[0] == expected_payload
