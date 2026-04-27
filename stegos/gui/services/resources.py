from PySide6.QtCore import QObject, QEvent, Qt
from PySide6.QtWidgets import QApplication

from stegos.gui.constants import Stylesheets
from stegos.gui.util import read_resource


class StyleSheetBuilder:
    def __init__(self, scheme: Qt.ColorScheme):
        self._base = read_resource(Stylesheets.BASE)
        self._color_scheme = scheme

    @property
    def base(self):
        return self._base

    @property
    def color_scheme(self):
        return self._color_scheme

    @color_scheme.setter
    def color_scheme(self, theme):
        self._color_scheme = theme

    def build(self) -> str:
        return "".join(
            [self.base, read_resource(Stylesheets.from_color_scheme(self.color_scheme))]
        )


class StyleSheetService(QObject):
    def __init__(self, app: QApplication = None):
        super().__init__()
        self._app = app or QApplication.instance()
        self._app.installEventFilter(self)

        self._builder = StyleSheetBuilder(self._app.styleHints().colorScheme())
        self._app.setStyleSheet(self._builder.build())

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """Updates the application stylesheets if there has been a color_scheme change."""
        if event.type() == QEvent.Type.ApplicationPaletteChange:
            theme = self._app.styleHints().colorScheme()
            if theme == self._builder.color_scheme:
                return False
            self._builder.color_scheme = theme
            self._app.setStyleSheet(self._builder.build())
        return False
