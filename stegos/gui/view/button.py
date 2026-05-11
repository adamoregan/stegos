from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon, Qt, QCursor
from PySide6.QtWidgets import QPushButton, QApplication, QToolTip, QWidget


class IconButton(QPushButton):
    """Icon button for representing actions."""

    def __init__(self, icon: QIcon, tooltip: str = "", parent: QWidget = None):
        """
        Creates an instance of IconButton.
        :param icon: Icon of the button.
        :param tooltip: Tooltip of the button.
        :param parent: Parent of the button.
        """
        super().__init__(parent=parent)

        self.setIcon(icon)
        self.setToolTip(tooltip)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class CopyButton(IconButton):
    """Icon button for copying from the clipboard."""

    def __init__(self, parent: QWidget = None):
        super().__init__(
            QIcon.fromTheme(QIcon.ThemeIcon.EditCopy), "Copy to Clipboard", parent
        )
        self.clicked.connect(self._show_tooltip)

    @Slot()
    def _show_tooltip(self):
        QToolTip.showText(QCursor.pos(), "Copied to Clipboard")


class PasteButton(IconButton):
    """Icon button for pasting from the clipboard."""

    def __init__(self, parent: QWidget = None):
        super().__init__(
            QIcon.fromTheme(QIcon.ThemeIcon.EditPaste), "Paste from Clipboard", parent
        )
        self._clipboard = QApplication.clipboard()
        self._clipboard.dataChanged.connect(self._update_enabled)

    @Slot()
    def _update_enabled(self):
        text = self._clipboard.text()
        self.setEnabled(bool(text.strip()))
