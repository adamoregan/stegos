from PySide6.QtCore import QObject, Signal, QEvent
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QDragMoveEvent
from PySide6.QtWidgets import QWidget


class FileSystemDropHandler(QObject):
    """Handler for drag-and-drop events for files and directories."""

    itemsDropped = Signal(list)

    def __init__(self, widget: QWidget):
        """
        Creates an instance of FileSystemDropHandler.
        :param widget: Widget to handle drag-and-drop events for. The instance is installed as an event filter for the
        widget.
        """
        super().__init__()

        self._widget = widget
        self._widget.setAcceptDrops(True)
        self._widget.installEventFilter(self)

    def _accept_items(self, event: QDragEnterEvent | QDragMoveEvent) -> None:
        """
        Accept the drag event if it contains files or directories.
        :param event: Drag event to check.
        """
        mime = event.mimeData()
        if not mime.hasUrls():
            return
        for url in mime.urls():
            if url.isLocalFile():
                event.acceptProposedAction()
                return

    def _handle_dropped_items(self, event: QDropEvent) -> None:
        """
        Accepts the drop event if it contains files or directories.

        Emits the dropped files/directories signal.
        :param event: Drop event to check.
        :return: If the drop event was accepted.
        """
        mime = event.mimeData()
        if not mime.hasUrls():
            return
        files = []
        for url in mime.urls():
            if url.isLocalFile():
                files.append(url.toLocalFile())
        if files:
            self.itemsDropped.emit(files)
            event.acceptProposedAction()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """Filters drag-and-drop events for files and directories."""
        match event.type():
            case QEvent.Type.DragEnter | QEvent.Type.DragMove:
                self._accept_items(event)
                return True
            case QEvent.Type.Drop:
                self._handle_dropped_items(event)
                return True
        return False
