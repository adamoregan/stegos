from enum import StrEnum

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QApplication


class Links(StrEnum):
    """Links to external resources."""

    REPOSITORY = "https://github.com/adamoregan/stegos"
    ISSUES = f"{REPOSITORY}/issues"


class Templates(StrEnum):
    """Templates of the application."""

    _FOLDER = ":/templates"
    HELP = f"{_FOLDER}/help.html"
    ABOUT = f"{_FOLDER}/about.html"


class Stylesheets(StrEnum):
    """Stylesheets of the application."""

    _FOLDER = ":/stylesheets"
    BASE = f"{_FOLDER}/base.qss"
    LIGHT = f"{_FOLDER}/light.qss"
    DARK = f"{_FOLDER}/dark.qss"

    @classmethod
    def from_color_scheme(cls, scheme: Qt.ColorScheme = None) -> "Stylesheets":
        """
        Gets the stylesheet for a color scheme.
        :param scheme: Color scheme to get the stylesheet from. If a color scheme is not provided, the application's
        current color scheme will be used.
        :return: Stylesheet for the given color scheme.
        """
        if not scheme:
            scheme = QApplication.instance().styleHints().colorScheme()
        if scheme == Qt.ColorScheme.Light:
            return cls.LIGHT
        return cls.DARK
