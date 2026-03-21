from PySide6.QtCore import QEvent, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QHBoxLayout,
    QRadioButton,
    QStackedWidget,
    QButtonGroup,
)

from stegos.core.cryptography.dh.x25519 import X25519
from stegos.core.service import LSBSteganographyService
from stegos.gui.constants import Stylesheets
from stegos.gui.model.dh import DHModel
from stegos.gui.util import read_resource
from stegos.gui.view.form import ExtractionForm, EmbeddingForm, SteganographyForm
from stegos.gui.view.image import ImagePreview
from stegos.gui.view.menu import AppMenuBar

from stegos.gui.resources import (
    rc_resources,
)  # Necessary for accessing Qt Resource System (stylesheets, templates, etc.)


class MainWindow(QMainWindow):
    """Main window of the application.

    Provides forms for steganography embedding and extracting.
    """

    def __init__(self):
        """Creates an instance of MainWindow."""
        super().__init__()
        self.setWindowTitle("Stegos")
        self.setMinimumSize(800, 600)

        self.dh_model = DHModel(X25519())
        self.setMenuBar(AppMenuBar(self, self.dh_model))
        self.service = LSBSteganographyService()

        self._create_ui()
        self._connect_signals()

    def _create_ui(self) -> None:
        """Creates the UI for the main window."""
        input_layout = QVBoxLayout()

        input_layout.addWidget(self._create_form_selection_section())

        preview_layout = QVBoxLayout()
        self.preview = ImagePreview()
        preview_layout.addWidget(self.preview)

        content_box = QHBoxLayout()
        content_box.addLayout(input_layout, stretch=3)
        content_box.addLayout(preview_layout, stretch=2)

        central_widget = QWidget()
        central_widget.setLayout(content_box)
        self.setCentralWidget(central_widget)

        self.form_stack = QStackedWidget()
        self.extraction_form = ExtractionForm(self.service)
        self.embedding_form = EmbeddingForm(self.service)

        self.form_stack.addWidget(self.embedding_form)
        self.form_stack.addWidget(self.extraction_form)

        input_layout.addWidget(self.form_stack)

    def _create_form_selection_section(self) -> QGroupBox:
        """Creates the section for setting the current form."""
        group = QGroupBox("Mode")
        mode_radio_layout = QHBoxLayout()
        self.embedding_radio = QRadioButton("Embedding")
        self.embedding_radio.setChecked(True)

        self.extracting_radio = QRadioButton("Extraction")

        self.mode_group = QButtonGroup()
        self.mode_group.addButton(self.embedding_radio, 0)
        self.mode_group.addButton(self.extracting_radio, 1)

        mode_radio_layout.addWidget(self.embedding_radio)
        mode_radio_layout.addWidget(self.extracting_radio)
        group.setLayout(mode_radio_layout)
        return group

    def _connect_signals(self) -> None:
        """Connects the signals for forms and the diffie-hellman dialog output."""
        self.mode_group.idToggled.connect(self._set_form)
        for form in (self.extraction_form, self.embedding_form):
            form.file_input.input.textChanged.connect(self.preview.set_image)
        self.dh_model.shared_key_generated.connect(self._set_password)

    @Slot(bytes)
    def _set_password(self, key: bytes) -> None:
        """
        Sets the password of the current form.
        :param key: Key to set as the password.
        """
        current_form: SteganographyForm = self.form_stack.currentWidget()
        current_form.password_input.input.setText(key.hex())

    @Slot(int)
    def _set_form(self, index: int) -> None:
        """
        Sets the current form.
        :param index: Index of the form to set as current.
        """
        self.form_stack.setCurrentIndex(index)
        current_form: SteganographyForm = self.form_stack.currentWidget()
        path = current_form.file_input.input.text()
        self.preview.set_image(path)


def load_stylesheets() -> str:
    """Loads the application stylesheets."""
    stylesheets = (Stylesheets.BASE, Stylesheets.from_color_scheme())
    return "".join(read_resource(stylesheet) for stylesheet in stylesheets)


class SteganographyApplication(QApplication):
    """Application for steganography operations."""

    def __init__(self, *args, **kwargs):
        """Creates an instance of SteganographyApplication."""
        super().__init__(*args, **kwargs)
        self.setWindowIcon(QIcon(":app.png"))

        self._current_theme = self.styleHints().colorScheme()
        self.setStyleSheet(load_stylesheets())

    def event(self, event: QEvent) -> bool:
        """Updates the application stylesheets if there has been a theme change."""
        handled = super().event(event)
        if event.type() == QEvent.Type.ApplicationPaletteChange:
            theme = self.styleHints().colorScheme()
            if theme == self._current_theme:
                return
            self._current_theme = theme
            self.setStyleSheet(load_stylesheets())
        return handled
