from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QCheckBox


class PasswordInput(QWidget):
    """Input for passwords with password visibility toggle."""

    passwordChanged = Signal(str)

    def __init__(self, placeholder_text: str = "Enter your password here..."):
        """
        Creates an instance of PasswordInput.
        :param placeholder_text: Placeholder text for the password input.
        """
        super().__init__()
        self._create_ui(placeholder_text)

    def password(self) -> str:
        """Gets the password."""
        return self._input.text()

    def set_password(self, password: str) -> None:
        """
        Sets the password text.
        :param password: Password to display in the input field.
        """
        self._input.setText(password)

    @property
    def is_visible(self) -> bool:
        """Gets the visibility of the password input."""
        return self._input.echoMode() == QLineEdit.EchoMode.Normal

    @Slot(bool)
    def _set_visible(self, visible: bool) -> None:
        """
        Sets the visibility of the password.
        :param visible: If the password should be shown.
        """
        self._input.setEchoMode(
            QLineEdit.EchoMode.Normal if visible else QLineEdit.EchoMode.Password
        )

    def _create_ui(self, placeholder_text: str) -> None:
        """
        Creates the UI for the password input.
        :param placeholder_text: Placeholder text for the password input.
        """
        layout = QVBoxLayout(self)

        self._input = QLineEdit(
            placeholderText=placeholder_text, echoMode=QLineEdit.EchoMode.Password
        )
        self._input.textChanged.connect(self.passwordChanged.emit)

        self._checkbox = QCheckBox("Show password")
        self._checkbox.setCursor(Qt.CursorShape.PointingHandCursor)
        self._checkbox.toggled.connect(self._set_visible)

        for widget in (self._input, self._checkbox):
            layout.addWidget(widget)
