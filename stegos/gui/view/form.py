import os.path

import jpegio
from PIL import Image
from PySide6.QtCore import Qt, Slot, QUrl
from PySide6.QtGui import QDesktopServices
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
    QMessageBox,
)

from stegos.core.service import LSBSteganographyService
from stegos.gui.model.steganography import (
    SteganographyModel,
    EmbeddingModel,
    ExtractionModel,
)
from stegos.gui.threading.executor import WorkerExecutor
from stegos.gui.view.dialog import OverwriteMessageBox, ProgressDialog
from stegos.gui.view.filesystem import FileSystemInput, MultiFileInput
from stegos.gui.view.input import PasswordInput


class SteganographyForm(QWidget):
    """Form for steganography operations."""

    def __init__(self, model: SteganographyModel, service: LSBSteganographyService):
        """
        Creates an instance of SteganographyForm.
        :param model: Model for steganography operations.
        """
        super().__init__()
        self._model = model
        self._service = service

        self._progress_dialog = None

    @property
    def model(self) -> SteganographyModel:
        """Gets the steganography model of the form."""
        return self._model

    @property
    def service(self) -> LSBSteganographyService:
        """Gets the steganography service of the form."""
        return self._service

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
        self.password_input.passwordChanged.connect(self.model.set_password)
        self.file_input.itemChanged.connect(self.model.set_image)
        self.filesystem_output.itemChanged.connect(self.model.set_output)

        self._model.canProcessChanged.connect(
            lambda: self.button.setEnabled(self._model.can_process)
        )


class EmbeddingForm(SteganographyForm):
    """Form for steganography embedding."""

    _model: EmbeddingModel  # static type hinting

    def __init__(self, service: LSBSteganographyService):
        """Creates an instance of EmbeddingForm."""
        super().__init__(EmbeddingModel(), service)
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
                self._update_text_payload()
            case self.file_form:
                self._update_file_payload()

    def _update_text_payload(self) -> None:
        self._model.set_payload(self.text_edit.toPlainText().encode())

    def _update_file_payload(self) -> None:
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

        self.text_edit.textChanged.connect(self._update_text_payload)
        self.file_form.file_list.model().rowsInserted.connect(self._update_file_payload)
        self.file_form.file_list.model().rowsRemoved.connect(self._update_file_payload)

        self.button.clicked.connect(self.embed)

    @Slot()
    def embed(self):
        """Embeds a payload into an image.

        Shows an overwrite, progress, and results dialog.
        """
        if os.path.isfile(self._model.output):
            res = OverwriteMessageBox(self._model.output, self).exec()
            if res == QMessageBox.StandardButton.No:
                return
        worker = WorkerExecutor.run(
            self.service.embed,
            self._model.image,
            self._model.payload,
            self._model.password.encode(),
        )
        self._progress_dialog = ProgressDialog(
            worker, "Embedding", "Embedding...", parent=self
        )
        worker.signals.result.connect(self._handle_embedding_result)
        worker.signals.error.connect(
            lambda e: QMessageBox.critical(
                self, "Error", "An error occurred during embedding."
            )
        )

    @Slot()
    def _handle_embedding_result(self, embedded):
        """Saves and opens the stego image."""
        if isinstance(embedded, Image.Image):
            embedded.save(self._model.output)
        else:
            jpegio.write(embedded, self._model.output)
        QDesktopServices.openUrl(QUrl.fromLocalFile(self._model.output))


class ExtractionForm(SteganographyForm):
    """Form for steganography extraction."""

    def __init__(self, service: LSBSteganographyService):
        """Creates an instance of ExtractionForm."""
        super().__init__(ExtractionModel(), service)
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

    def _connect_signals(self) -> None:
        """Connects signals for inputs."""
        super()._connect_signals()
        self.button.clicked.connect(self.extract)

    @Slot()
    def extract(self):
        """Extract a payload from an image.

        Shows a progress and results dialog.
        """
        worker = WorkerExecutor.run(
            self.service.extract, self._model.image, self._model.password.encode()
        )
        self._progress_dialog = ProgressDialog(
            worker, "Extracting", "Extracting..", parent=self
        )
        worker.signals.result.connect(self._handle_extraction)
        worker.signals.error.connect(
            lambda e: QMessageBox.critical(
                self, "Error", "An error occurred during extraction."
            )
        )

    @Slot()
    def _handle_extraction(self, extracted):
        """Saves and shows dialogs for the extracted files/bytes."""
        name, content = extracted[0], extracted[1]
        if name == "output":
            QMessageBox.information(
                self,
                "Extracted Message",
                f"The following message was extracted:<br><br>'{content.decode()}'",
            )
        else:
            with open(f"{self.model.output}{name}", "wb") as file:
                file.write(content)
            QMessageBox.information(
                self,
                "Extracted File",
                f"The following file was extracted:<br><br>'{name}'",
            )
