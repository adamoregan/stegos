from unittest.mock import Mock

import pytest
from PySide6.QtCore import Qt

from stegos.gui.view.filesystem import (
    FileSystemDropList,
    FileSystemLineEdit,
    MultiFileInput,
)


class TestFileSystemDropList:
    """Tests for FileSystemDropList."""

    def test_dropped_files(self, qtbot):
        """Drag-and-dropped items should be added to the list."""
        files = ("/tmp/file.txt", "/tmp/file2.txt")
        widget = FileSystemDropList()
        qtbot.addWidget(widget)
        widget._drop_handler.itemsDropped.emit(files)
        assert widget.count() == len(files)


class TestFileSystemLineEdit:
    """Tests for FileSystemLineEdit."""

    def test_dropped_files(self, qtbot):
        """Text should be set to the first drag-and-dropped item."""
        files = ("/tmp/file.txt", "/tmp/file2.txt")
        widget = FileSystemLineEdit()
        qtbot.addWidget(widget)
        widget._drop_handler.itemsDropped.emit(files)
        assert widget.text() == files[0]


@pytest.fixture
def multi_input(qtbot) -> MultiFileInput:
    widget = MultiFileInput()
    qtbot.addWidget(widget)
    return widget


class TestMultiFileInput:
    """Tests for MultiFileInput."""

    def test_add_button_click(self, multi_input, qtbot):
        """The add button should allow files to be added."""
        files = ("/tmp/file.txt", "/tmp/file2.txt")
        multi_input._dialog.exec = Mock(return_value=True)
        multi_input._dialog.selectedFiles = Mock(return_value=files)
        qtbot.mouseClick(multi_input.add_button, Qt.MouseButton.LeftButton)
        assert multi_input.file_list.count() == len(files)

    def test_remove_button(self, multi_input, qtbot):
        """The remove button should only be enabled if a file is selected."""
        remove_button = multi_input.remove_button
        assert not remove_button.isEnabled()

        multi_input.file_list.addItems(["/tmp/file.txt"])
        multi_input.file_list.setCurrentRow(0)
        assert remove_button.isEnabled()

        qtbot.mouseClick(remove_button, Qt.MouseButton.LeftButton)
        assert not remove_button.isEnabled()

    def test_clear_button(self, multi_input, qtbot):
        """The clear button should be disabled if there are no files."""
        clear_button = multi_input.clear_button
        assert not clear_button.isEnabled()

        multi_input.file_list.addItems(["/tmp/file.txt"])
        assert clear_button.isEnabled()

        qtbot.mouseClick(clear_button, Qt.MouseButton.LeftButton)
        assert not clear_button.isEnabled()
