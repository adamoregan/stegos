from PySide6.QtCore import Slot, QUrl
from PySide6.QtGui import QAction, QDesktopServices, QKeySequence
from PySide6.QtWidgets import QMenuBar, QMainWindow, QMessageBox, QMenu

from stegos.gui.constants import Templates, Links
from stegos.gui.model.dh import DHModel
from stegos.gui.util import read_resource
from stegos.gui.view.dialog import HelpDialog, DHKEDialog


class HelpMenu(QMenu):
    """Help menu of the application."""

    def __init__(self, parent: QMenuBar = None):
        """
        Creates an instance of HelpMenu.
        :param parent: Menubar that the menu belongs to.
        """
        super().__init__("Help", parent)
        self._create_actions()

    def _create_actions(self) -> None:
        """Creates the actions of the menu."""
        help_info = QAction(
            "Help", self, shortcut=QKeySequence.StandardKey.HelpContents
        )
        help_info.triggered.connect(lambda: HelpDialog(self).show())

        report_issue = QAction("Report Issue", self)
        report_issue.triggered.connect(
            lambda: QDesktopServices.openUrl(QUrl(Links.ISSUES))
        )

        about = QAction("About", self)
        about.triggered.connect(self._show_about_dialog)

        self.addAction(help_info)
        self.addSeparator()
        self.addAction(report_issue)
        self.addSeparator()
        self.addAction(about)

    @Slot()
    def _show_about_dialog(self) -> None:
        """Shows the 'about' dialog of the application"""
        QMessageBox.about(
            self,
            "About Stegos",
            read_resource(Templates.ABOUT).format(repository=Links.REPOSITORY),
        )


class AppMenuBar(QMenuBar):
    """Menubar of the application."""

    def __init__(self, parent: QMainWindow, dh_model: DHModel):
        """
        Creates an instance of AppMenuBar.
        :param parent: Main window of the application.
        :param dh_model: Diffie-Hellman model for key exchange.
        """
        super().__init__(parent)
        self._dh_model = dh_model

        self._create_file_menu()
        self._create_tools_menu()
        self.addMenu(HelpMenu(self))

    def _create_file_menu(self) -> None:
        """Creates the file menu."""
        menu = self.addMenu("File")
        exit_app = QAction("Exit", self, shortcut="Ctrl+Q")
        exit_app.triggered.connect(self.parent().close)
        menu.addAction(exit_app)

    def _create_tools_menu(self) -> None:
        """Creates the tool menu."""
        menu = self.addMenu("Tools")
        dh = QAction("Diffie-Hellman", self, shortcut="Ctrl+D")
        dh.triggered.connect(lambda: DHKEDialog(self._dh_model, self).show())
        menu.addAction(dh)
