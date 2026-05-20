from unittest.mock import Mock

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from stegos.gui.view.button import CopyButton, PasteButton


class TestCopyButton:
    """Tests for CopyButton."""

    def test_copy(self, qtbot):
        """Text should be copied to the clipboard."""
        text = "text copied to clipboard"
        get_text = Mock(return_value=text)
        widget = CopyButton(get_text)
        qtbot.mouseClick(widget, Qt.MouseButton.LeftButton)
        get_text.assert_called_once()
        assert QApplication.clipboard().text() == text


class TestPasteButton:
    """Tests for PasteButton."""

    def test_paste(self, qtbot):
        """Text should be pasted from the clipboard."""
        text, set_text = "clipboard text", Mock()
        QApplication.clipboard().setText(text)
        widget = PasteButton(set_text)
        qtbot.addWidget(widget)
        qtbot.mouseClick(widget, Qt.MouseButton.LeftButton)
        set_text.assert_called_once()
        set_text.assert_called_with(text)

    def test_enabled(self, qtbot, qapp):
        """The button should only be enabled if there is clipboard text."""
        QApplication.clipboard().setText("")
        widget = PasteButton(Mock())
        qtbot.addWidget(widget)
        assert not widget.isEnabled()

        QApplication.clipboard().setText("clipboard text")
        qtbot.waitUntil(widget.isEnabled)
        assert widget.isEnabled()
