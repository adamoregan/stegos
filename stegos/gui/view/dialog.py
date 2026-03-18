from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QIcon, QCursor
from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QPlainTextEdit,
    QPushButton,
    QToolTip,
    QTextBrowser,
)

from stegos.gui.constants import Templates, Links
from stegos.gui.model.dh import DHModel
from stegos.gui.util import read_resource
from stegos.gui.view.button import IconButton
from stegos.gui.view.label import BoldLabel, ErrorLabel


class HelpDialog(QDialog):
    """Help dialog for information on using the application."""

    def __init__(self, parent: QWidget = None):
        """
        Creates an instance of HelpDialog.
        :param parent: Parent of the dialog. When the parent is closed, the dialog is automatically closed.
        """
        super().__init__(parent)
        self.setWindowTitle("Help")
        self.setMinimumSize(350, 400)
        self._create_ui()

    def _create_ui(self):
        """Creates the UI of the dialog."""
        layout = QVBoxLayout(self)
        self.browser = QTextBrowser(openExternalLinks=True)
        self.browser.setHtml(
            read_resource(Templates.HELP).format(repository=Links.REPOSITORY)
        )
        self.browser.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.browser)
        layout.addWidget(self.close_button)


class DHKEDialog(QDialog):
    """Diffie-Hellman Key Exchange dialog for generating a shared key."""

    def __init__(self, model: DHModel, parent: QWidget = None):
        """
        Creates an instance of DHKEDialog.
        :param model: Model for the diffie-hellman key exchange.
        :param parent: Parent of the dialog. When the parent is closed, the dialog is automatically closed.
        """
        super().__init__(parent)
        self._model = model
        self.setWindowTitle("Diffie-Hellman Key Exchange")
        self.setFixedSize(300, 250)

        self._create_ui()
        self._connect_signals()

    def _create_ui(self):
        """Creates the UI of the dialog."""
        layout = QVBoxLayout(self)
        layout.addLayout(self._create_key_output_section())
        layout.addLayout(self._create_key_input_section())
        layout.addWidget(self._create_generate_button())

    def _create_key_output_section(self) -> QVBoxLayout:
        """Creates the key output section for showing the user's public key."""
        layout = QVBoxLayout()

        layout.addWidget(BoldLabel("Your Public Key:"))

        key_output_layout = QHBoxLayout()

        self.key_output = QPlainTextEdit(self._model.public_key.hex(), readOnly=True)
        key_output_layout.addWidget(self.key_output)

        self.copy_btn = IconButton(
            QIcon.fromTheme(QIcon.ThemeIcon.EditCopy), "Copy to Clipboard"
        )
        self.copy_btn.clicked.connect(self.copy_key)
        self.refresh_btn = IconButton(
            QIcon.fromTheme(QIcon.ThemeIcon.ViewRefresh), "Refresh Key"
        )
        self.refresh_btn.clicked.connect(self._model.rotate)

        for button in (self.copy_btn, self.refresh_btn):
            key_output_layout.addWidget(button)
            key_output_layout.setAlignment(button, Qt.AlignmentFlag.AlignTop)

        layout.addLayout(key_output_layout)
        return layout

    def _create_key_input_section(self) -> QVBoxLayout:
        """Creates the key input section for entering the peer's public key."""
        layout = QVBoxLayout()

        layout.addWidget(BoldLabel("Peer Public Key:"))

        input_layout = QHBoxLayout()

        self.key_input = QPlainTextEdit()
        self.key_input.setPlaceholderText("Enter public key")

        input_layout.addWidget(self.key_input)

        self.paste_btn = IconButton(
            QIcon.fromTheme(QIcon.ThemeIcon.EditPaste), "Paste from Clipboard"
        )
        self.paste_btn.clicked.connect(self.paste_key)
        QApplication.clipboard().dataChanged.connect(self.update_paste_enabled)

        input_layout.addWidget(self.paste_btn)
        input_layout.setAlignment(self.paste_btn, Qt.AlignmentFlag.AlignTop)

        layout.addLayout(input_layout)

        self.error_label = ErrorLabel("Invalid public key!")
        layout.addWidget(self.error_label)

        return layout

    def _create_generate_button(self) -> QPushButton:
        """Creates the shared key generation button."""
        self.submit_btn = QPushButton("Generate Shared Key")
        self.submit_btn.setEnabled(False)
        self.submit_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.submit_btn.clicked.connect(self.generate_shared_key)
        return self.submit_btn

    def _connect_signals(self) -> None:
        """Connects the signals for the model and error handling."""
        self._model.public_key_changed.connect(
            lambda key: self.key_output.setPlainText(key.hex())
        )
        self._model.error.connect(lambda: self.error_label.setVisible(True))
        self._model.shared_key_generated.connect(self.accept)
        self.key_input.textChanged.connect(self.on_key_input_change)

    def generate_shared_key(self):
        """Generates the shared key.

        If the key can not be generated, an error is shown.
        """
        try:
            peer_key = bytes.fromhex(self.key_input.toPlainText().strip())
        except ValueError:
            self.error_label.setVisible(True)
            return
        self._model.exchange(peer_key)

    @Slot()
    def on_key_input_change(self):
        """Enables and sets visibility of elements."""
        self.submit_btn.setEnabled(bool(self.key_input.toPlainText().strip()))
        self.error_label.setVisible(False)

    @Slot()
    def update_paste_enabled(self):
        """Updates the state of the paste button based on the content of the clipboard."""
        clipboard_text = QApplication.clipboard().text()
        self.paste_btn.setEnabled(bool(clipboard_text.strip()))

    @Slot()
    def paste_key(self):
        """Pastes the peer key from the clipboard."""
        self.key_input.setPlainText(QApplication.clipboard().text())

    @Slot()
    def copy_key(self):
        """Copies the public key to the clipboard."""
        QApplication.clipboard().setText(self.key_output.toPlainText())
        QToolTip.showText(QCursor.pos(), "Copied to Clipboard")
