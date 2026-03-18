from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import (
    QListWidget,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QLineEdit,
)

from stegos.gui.controller.filesystem import FileSystemDropHandler


class FileSystemDropList(QListWidget):
    """List that accepts drag-and-drop events for files and directories."""

    def __init__(self, tooltip: str = ""):
        """
        Creates an instance of FileSystemDropList.
        :param tooltip: Tooltip of the list.
        """
        super().__init__()

        self.setToolTip(tooltip)

        self.drop_handler = FileSystemDropHandler(self)
        self.drop_handler.items_dropped.connect(self.addItems)


class FileSystemLineEdit(QLineEdit):
    """LineEdit that accepts drag-and-drop events for files and directories."""

    def __init__(self, placeholderText: str = "Drop file here..."):
        """
        Creates an instance of FileSystemLineEdit.
        :param placeholderText: Placeholder text for the input.
        """
        super().__init__(placeholderText=placeholderText)
        self.drop_handler = FileSystemDropHandler(self)
        self.drop_handler.items_dropped.connect(lambda items: self.setText(items[0]))


class FileSystemInput(QWidget):
    """Input with file system browsing and drag-and-drop functionality."""

    item_changed = Signal(str)

    def __init__(
        self,
        mode: QFileDialog.FileMode = QFileDialog.FileMode.AnyFile,
        placeholderText: str = None,
    ):
        """Creates an instance of FileSystemInput."""
        super().__init__()

        self.dialog = QFileDialog(fileMode=mode)

        layout = QHBoxLayout(self)

        self.input = FileSystemLineEdit(placeholderText or "Drop file here...")

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self._browse)

        layout.addWidget(self.input)
        layout.addWidget(self.browse_button)

        self.input.textChanged.connect(self.item_changed)

    @Slot()
    def _browse(self):
        """Browse the file system.

        Populates the input if a file or directory is selected.
        """
        if self.dialog.exec():
            items = self.dialog.selectedFiles()
            if items:
                self.input.setText(items[0])


class MultiFileInput(QWidget):
    """Multi file input with file system browsing, drag-and-drop functionality, and buttons for list operations."""

    def __init__(self):
        """Creates an instance of MultiFileInput."""
        super().__init__()

        self._dialog = QFileDialog(fileMode=QFileDialog.FileMode.ExistingFiles)

        self._create_ui()
        self._connect_signals()

    def _create_ui(self) -> None:
        """Creates the UI of the file input."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.file_list = FileSystemDropList("Drop File(s) Here")

        layout.addWidget(self.file_list)
        layout.addLayout(self._create_button_layout())

    def _create_button_layout(self) -> QVBoxLayout:
        """Creates the button layout for list operations."""
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.add_button = QPushButton("Add File(s)")
        self.remove_button = QPushButton("Remove")
        self.remove_button.setEnabled(False)
        self.clear_button = QPushButton("Clear")
        self.clear_button.setEnabled(False)

        for button in (self.add_button, self.remove_button, self.clear_button):
            button_layout.addWidget(button)
        return button_layout

    def _connect_signals(self):
        """Connects the signals for the file list operations buttons."""
        self.add_button.clicked.connect(self._browse)
        self.remove_button.clicked.connect(self._remove_selected)
        self.clear_button.clicked.connect(self.file_list.clear)

        self.file_list.itemSelectionChanged.connect(self._toggle_update_button)
        self.file_list.model().rowsInserted.connect(self._toggle_clear_button)
        self.file_list.model().rowsRemoved.connect(self._toggle_clear_button)

    @Slot()
    def _toggle_update_button(self) -> None:
        """Toggles the update button depending on if a file is selected."""
        self.remove_button.setEnabled(bool(self.file_list.selectedItems()))

    @Slot()
    def _toggle_clear_button(self) -> None:
        """Toggles the clear button depending on if there are files in the file list."""
        self.clear_button.setEnabled(self.file_list.count())

    @Slot()
    def _browse(self) -> None:
        """Browses the file system for file selection."""
        if self._dialog.exec():
            files = self._dialog.selectedFiles()
            self.file_list.addItems(files)

    @Slot()
    def _remove_selected(self) -> None:
        """Removes the selected file from the file list."""
        for item in self.file_list.selectedItems():
            self.file_list.takeItem(self.file_list.row(item))
