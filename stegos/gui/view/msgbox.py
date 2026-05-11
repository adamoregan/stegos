from abc import abstractmethod

from PySide6.QtWidgets import QMessageBox, QWidget
from cryptography.fernet import InvalidToken

from stegos.core.steganography.exception import (
    InsufficientCapacityException,
    InvalidCoverImageException,
)


class OverwriteMessageBox(QMessageBox):
    """Message box prompting the user to confirm if they want to overwrite an existing file."""

    def __init__(self, file: str, parent: QWidget = None):
        """
        Creates an instance of OverwriteMessageBox.
        :param file: Existing file to overwrite.
        :param parent: Parent of the message box.
        """
        super().__init__(
            QMessageBox.Icon.Warning,
            "Overwrite File?",
            f"File '{file}' already exists.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            parent,
            informativeText="Do you want to overwrite it?",
        )
        self.setDefaultButton(
            QMessageBox.StandardButton.No
        )  # helps avoid accidental overwrites


class InsufficientCapacityMessageBox(QMessageBox):
    """Message box for InsufficientCapacityException."""

    def __init__(self, e: InsufficientCapacityException, parent: QWidget = None):
        """
        Creates an instance of InsufficientCapacityException.
        :param e: InsufficientCapacityException to display.
        :param parent: Parent of the message box.
        """
        super().__init__(
            QMessageBox.Icon.Critical,
            "Embedding Error",
            "Input is too large for the selected image.",
            informativeText="Reduce the input size or choose a larger image.",
            detailedText=f"Exceeded image capacity by {e.payload_size - e.capacity} bytes.",
            parent=parent,
        )


class ExceptionMessageBoxFactory:
    """Factory for creating message boxes based on exception type."""

    @classmethod
    @abstractmethod
    def create(cls, e: Exception, parent: QWidget = None) -> QMessageBox:
        """
        Creates a message box based on exception type.
        :param e: Exception to create the message box from.
        :param parent: Parent of the message box.
        :return: Exception message box.
        """
        return


class EmbeddingMessageBoxFactory(ExceptionMessageBoxFactory):
    """Factory for creating message boxes based on steganography embedding exception type."""

    @classmethod
    def create(cls, e: Exception, parent: QWidget = None) -> QMessageBox:
        text, informativeText = "An error occurred during embedding.", ""
        match e:
            case InsufficientCapacityException():  # does not instantiate
                return InsufficientCapacityMessageBox(e, parent)
            case InvalidCoverImageException():
                text, informativeText = (
                    "Selected image is too small.",
                    "Choose a larger image.",
                )
        return QMessageBox(
            QMessageBox.Icon.Critical,
            "Embedding Error",
            text,
            informativeText=informativeText,
            parent=parent,
        )


class ExtractionMessageBoxFactory(ExceptionMessageBoxFactory):
    """Factory for creating message boxes based on steganography extraction exception type."""

    @classmethod
    def create(cls, e: Exception, parent: QWidget = None) -> QMessageBox:
        text, informativeText = "An error occurred during extraction.", ""
        match e:
            case InvalidToken():
                text, informativeText = (
                    "Embedded data could not be extracted.",
                    "Selected image may not contain embedded data, or the password may be incorrect.",
                )
        return QMessageBox(
            QMessageBox.Icon.Critical,
            "Extraction Error",
            text,
            informativeText=informativeText,
            parent=parent,
        )
