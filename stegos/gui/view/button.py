from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QPushButton


class IconButton(QPushButton):
    """Icon button for representing actions."""

    def __init__(self, icon: QIcon, tooltip: str = ""):
        """
        Creates an instance of IconButton.
        :param icon: Icon of the button.
        :param tooltip: Tooltip of the button.
        """
        super().__init__()

        self.setIcon(icon)
        self.setToolTip(tooltip)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
