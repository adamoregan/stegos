from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QHBoxLayout,
    QRadioButton,
    QPlainTextEdit,
    QPushButton,
    QStackedWidget,
    QButtonGroup,
    QFileDialog,
)

from stegos.gui.model.steganography import (
    SteganographyModel,
    EmbeddingModel,
    ExtractionModel,
)
from stegos.gui.view.filesystem import FileSystemInput, MultiFileInput
from stegos.gui.view.input import PasswordInput


class SteganographyForm(QWidget):
    """Form for steganography operations."""

    def __init__(self, model: SteganographyModel):
        """
        Creates an instance of SteganographyForm.
        :param model: Model for steganography operations.
        """
        super().__init__()
        self._model = model

    @property
    def model(self) -> SteganographyModel:
        """Gets the steganography model of the form."""
        return self._model

    def _create_password_section(self) -> QGroupBox:
        """Creates the password section of the form."""
        group = QGroupBox("Password")
        self.password_input = PasswordInput()
        group.setLayout(self.password_input.layout())
        return group

    def _create_image_section(self, title: str) -> QGroupBox:
        """Creates the image section of the form."""
        group = QGroupBox(title)
        layout = QVBoxLayout(group)
        layout.setContentsMargins(0, 0, 0, 0)
        self.file_input = FileSystemInput()
        layout.addWidget(self.file_input)
        return group

    def _create_button(self, text: str) -> QPushButton:
        """Creates the steganography operations button."""
        self.button = QPushButton(text)
        self.button.setEnabled(False)
        return self.button

    def _create_filesystem_output_section(
        self,
        mode: QFileDialog.FileMode = QFileDialog.FileMode.AnyFile,
        placeholderText: str = None,
    ):
        """Creates the filesystem output section, where the result of the steganography operation will be stored."""
        group = QGroupBox("Output")
        layout = QVBoxLayout(group)
        layout.setContentsMargins(0, 0, 0, 0)
        self.filesystem_output = FileSystemInput(mode, placeholderText)
        layout.addWidget(self.filesystem_output)
        return group

    def _connect_signals(self) -> None:
        """Connects each relevant section to the model."""
        self.password_input.input.textChanged.connect(self.model.set_password)
        self.file_input.item_changed.connect(self.model.set_image)
        self.filesystem_output.item_changed.connect(self.model.set_output)

        self._model.can_process_changed.connect(
            lambda: self.button.setEnabled(self._model.can_process)
        )


class EmbeddingForm(SteganographyForm):
    """Form for steganography embedding."""

    _model: EmbeddingModel  # static type hinting

    def __init__(self):
        """Creates an instance of EmbeddingForm."""
        super().__init__(EmbeddingModel())
        self._create_ui()
        self._connect_signals()

    def _create_ui(self) -> None:
        """Creates the UI for the embedding form."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        for widget in (
            self._create_image_section("Cover Image"),
            self._create_input_section(),
            self._create_filesystem_output_section(),
            self._create_password_section(),
            self._create_button("Embed"),
        ):
            layout.addWidget(widget)

    def _create_input_section(self) -> QGroupBox:
        """Creates the input section for the form. Allows text or file(s) as valid inputs."""
        group = QGroupBox("Input")
        layout = QVBoxLayout(group)

        self.text_radio = QRadioButton("Text")
        self.text_radio.setChecked(True)
        self.file_radio = QRadioButton("File(s)")

        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.text_radio)
        mode_layout.addWidget(self.file_radio)
        layout.addLayout(mode_layout)

        text_layout = QVBoxLayout()
        self.text_edit = QPlainTextEdit()
        self.text_edit.setPlaceholderText("Enter text here...")
        text_layout.addWidget(self.text_edit)

        self.file_form = MultiFileInput()

        self.input_stack = QStackedWidget()
        self.input_stack.addWidget(self.text_edit)
        self.input_stack.addWidget(self.file_form)
        layout.addWidget(self.input_stack)

        self.mode_group = QButtonGroup(self)
        self.mode_group.addButton(self.text_radio, 0)
        self.mode_group.addButton(self.file_radio, 1)

        return group

    @Slot()
    def _update_payload_from_mode(self) -> None:
        """Updates the payload of the model depending on the current input mode."""
        current = self.input_stack.currentWidget()
        match current:
            case self.text_edit:
                self._model.set_payload(self.text_edit.toPlainText())
            case self.file_form:
                files = [
                    self.file_form.file_list.item(file).text()
                    for file in range(self.file_form.file_list.count())
                ]
                self._model.set_payload(files)

    def _connect_signals(self) -> None:
        """Connects signals for inputs."""
        super()._connect_signals()
        self.mode_group.idToggled.connect(self.input_stack.setCurrentIndex)

        self.input_stack.currentChanged.connect(self._update_payload_from_mode)
        self.text_edit.textChanged.connect(
            lambda: self._model.set_payload(self.text_edit.toPlainText())
        )


class ExtractionForm(SteganographyForm):
    """Form for steganography extraction."""

    def __init__(self):
        """Creates an instance of ExtractionForm."""
        super().__init__(ExtractionModel())
        self._create_ui()
        self._connect_signals()

    def _create_ui(self) -> None:
        """Creates the UI for the extraction form."""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        for widget in (
            self._create_image_section("Stego Image"),
            self._create_filesystem_output_section(
                QFileDialog.FileMode.Directory, "Drop directory here..."
            ),
            self._create_password_section(),
            self._create_button("Extract"),
        ):
            layout.addWidget(widget)
