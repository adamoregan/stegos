from PySide6.QtCore import QObject, Signal, QEvent
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QDragMoveEvent
from PySide6.QtWidgets import QWidget


class FileSystemDropHandler(QObject):
    """Handler for drag-and-drop events for files and directories."""

    items_dropped = Signal(list)

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

    @staticmethod
    def _accept_items(event: QDragEnterEvent | QDragMoveEvent) -> bool:
        """
        Accept the drag event if it contains files or directories.
        :param event: Drag event to check.
        :return: If the drag event was accepted.
        """
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            return True
        return False

    def _handle_dropped_items(self, event: QDropEvent) -> bool:
        """
        Accepts the drop event if it contains files or directories.

        Emits the dropped files/directories signal.
        :param event: Drop event to check.
        :return: If the drop event was accepted.
        """
        if event.mimeData().hasUrls():
            files = []
            for url in event.mimeData().urls():
                file = url.toLocalFile()
                if file:
                    files.append(file)
            self.items_dropped.emit(files)
            event.acceptProposedAction()
            return True
        return False

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """Filters drag-and-drop events for files and directories."""
        filtered = super().eventFilter(watched, event)
        match event.type():
            case QEvent.Type.DragEnter | QEvent.Type.DragMove:
                return FileSystemDropHandler._accept_items(event)
            case QEvent.Type.Drop:
                return self._handle_dropped_items(event)
        return filtered
