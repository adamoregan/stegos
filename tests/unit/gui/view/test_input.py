import pytest
from PySide6.QtTest import QSignalSpy
from PySide6.QtWidgets import QLineEdit

from stegos.gui.view.input import PasswordInput


@pytest.fixture
def password_input(qtbot) -> PasswordInput:
    widget = PasswordInput()
    qtbot.addWidget(widget)
    return widget


class TestPasswordInput:
    """Tests for PasswordInput."""

    def test_defaults(self, password_input):
        """The password should be hidden by default with the checkbox disabled."""
        assert password_input.is_visible is False
        assert password_input._checkbox.isChecked() is False
        assert password_input._input.echoMode() == QLineEdit.EchoMode.Password

    def test_password_visibility(self, password_input):
        """The visibility of the password should be determined by the checkbox."""
        password_input._checkbox.setChecked(True)
        assert password_input.is_visible is True
        assert password_input._input.echoMode() == QLineEdit.EchoMode.Normal
        password_input._checkbox.setChecked(False)
        assert password_input.is_visible is False

    def test_passwordChanged_set(self, qtbot, password_input):
        """A signal should be emitted when the password is set."""
        password = "secret"
        spy = QSignalSpy(password_input.passwordChanged)
        password_input.set_password(password)
        assert spy.count() == 1
        assert spy.at(0)[0] == password

    def test_passwordChanged_typing(self, qtbot, password_input):
        """A signal should be emitted as the password is typed."""
        password = "secret"
        spy = QSignalSpy(password_input.passwordChanged)
        qtbot.keyClicks(password_input._input, password)
        assert spy.count() == len(password)
        assert spy.at(spy.count() - 1)[0] == password
