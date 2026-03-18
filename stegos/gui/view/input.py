from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QCheckBox


class PasswordInput(QWidget):
    """Input for passwords with password visibility toggle."""

    def __init__(self, placeholder_text: str = "Enter your password here..."):
        """
        Creates an instance of PasswordInput.
        :param placeholder_text: Placeholder text for the password input.
        """
        super().__init__()
        self._create_ui(placeholder_text)

    def _create_ui(self, placeholder_text: str) -> None:
        """
        Creates the UI for the password input.
        :param placeholder_text: Placeholder text for the password input.
        """
        layout = QVBoxLayout(self)

        self.input = QLineEdit(
            placeholderText=placeholder_text, echoMode=QLineEdit.EchoMode.Password
        )
        self.checkbox = QCheckBox("Show password")
        self.checkbox.setCursor(Qt.CursorShape.PointingHandCursor)
        self.checkbox.stateChanged.connect(self.show_password)

        for widget in (self.input, self.checkbox):
            layout.addWidget(widget)

    @Slot(int)
    def show_password(self, state: int | bool) -> None:
        """
        Shows the password.
        :param state: If the password should be shown.
        """
        mode = QLineEdit.EchoMode.Normal if state else QLineEdit.EchoMode.Password
        self.input.setEchoMode(mode)
