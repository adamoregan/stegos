from abc import abstractmethod
from pathlib import Path
from PySide6.QtCore import QObject, Signal

from stegos.core.steganography.util import is_image


class SteganographyModel(QObject):
    """Base model for steganography operations."""

    canProcessChanged = Signal()

    def __init__(self):
        """Creates an instance of SteganographyModel."""
        super().__init__()
        self._image = ""
        self._password = ""
        self._output = ""

    @property
    def image(self) -> str:
        """Gets the path of the image."""
        return self._image

    def set_image(self, image: str) -> None:
        """
        Sets the image used for steganography operations.
        :param image: Image path.
        """
        image = image.strip()
        if self.image == image:
            return
        self._image = image
        self.canProcessChanged.emit()

    @property
    def password(self) -> str:
        """Gets the password."""
        return self._password

    def set_password(self, password: str) -> None:
        """
        Sets the password used for steganography operations.
        :param password: Password used for protecting data.
        """
        password = password.strip()
        if self.password == password:
            return
        self._password = password
        self.canProcessChanged.emit()

    @property
    def output(self) -> str:
        return self._output

    def set_output(self, output: str) -> None:
        """
        Sets the output for steganography operations.

        Defines where the result of operations will be stored.
        :param output: Output path for steganography applications.
        """
        output = output.strip()
        if self.output == output:
            return
        self._output = output
        self.canProcessChanged.emit()

    @abstractmethod
    def is_valid_output(self) -> bool:
        """If the output is valid for steganography operations."""
        pass

    @property
    def can_process(self) -> bool:
        """If steganography operations can be performed."""
        return bool(self.password) and self.is_valid_output() and is_image(self.image)


class EmbeddingModel(SteganographyModel):
    """Model for steganography embedding."""

    def __init__(self):
        """Creates an instance of EmbeddingModel."""
        super().__init__()
        self._payload = None

    @property
    def payload(self):
        """Gets the embedding payload."""
        return self._payload

    def set_payload(self, payload) -> None:
        """
        Sets the embedding payload.
        :param payload: Payload to embed.
        """
        if self._payload == payload:
            return
        self._payload = payload
        self.canProcessChanged.emit()

    def is_valid_output(self) -> bool:
        return Path(self.output).is_file()

    @property
    def can_process(self) -> bool:
        """If embedding can be performed."""
        return super().can_process and bool(self.payload)


class ExtractionModel(SteganographyModel):
    """Model for steganography extraction."""

    def __init__(self):
        """Creates an instance of ExtractionModel."""
        super().__init__()

    def is_valid_output(self) -> bool:
        return Path(self.output).is_dir()
