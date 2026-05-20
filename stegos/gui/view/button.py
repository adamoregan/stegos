from collections.abc import Callable

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

    def __init__(self, get_text: Callable[[], str], parent: QWidget = None):
        """
        Creates an instance of CopyButton.
        :param get_text: Function that returns the text to copy to the clipboard.
        :param parent: Parent of the button
        """
        super().__init__(
            QIcon.fromTheme(QIcon.ThemeIcon.EditCopy), "Copy to Clipboard", parent
        )
        self._get_text = get_text
        self.clicked.connect(self._copy)

    @Slot()
    def _copy(self):
        """Copies text to the clipboard and provides feedback."""
        QApplication.clipboard().setText(self._get_text())
        QToolTip.showText(QCursor.pos(), "Copied to Clipboard")


class PasteButton(IconButton):
    """Icon button for pasting from the clipboard."""

    def __init__(self, set_text: Callable[[str], None], parent: QWidget = None):
        """
        Creates an instance of PasteButton.
        :param set_text: Function that accepts the clipboard text.
        :param parent: Parent of the button.
        """
        super().__init__(
            QIcon.fromTheme(QIcon.ThemeIcon.EditPaste), "Paste from Clipboard", parent
        )
        self._set_text = set_text
        self._set_enabled()

        self.clicked.connect(self._paste)
        QApplication.clipboard().dataChanged.connect(self._set_enabled)

    @Slot()
    def _paste(self):
        """Pastes the clipboard text."""
        self._set_text(QApplication.clipboard().text())

    def _set_enabled(self):
        """Enables the button based on clipboard text."""
        text = QApplication.clipboard().text()
        self.setEnabled(bool(text.strip()))
