from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout

from stegos.core.steganography.util import is_image
from stegos.gui.view.label import ScaledPixmapLabel


class ImagePreview(QWidget):
    """Preview display for images."""

    def __init__(self, image: str = ""):
        """
        Creates an instance of ImagePreview,
        :param image: Image to preview.
        """
        super().__init__()
        self._image = image

        layout = QVBoxLayout(self)
        self._label = ScaledPixmapLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._label)

        self._set_label(self.image)

    @property
    def image(self) -> str:
        """Gets the preview image."""
        return self._image

    def _set_label(self, image: str) -> None:
        """
        Sets the label text and image.
        :param image: Image to preview.
        """
        if not image:
            self._label.clear()
            self._label.setText("No Image Selected")
            return
        if is_image(image):
            self._label.setPixmap(QPixmap(image))
            return
        self._label.setText("Invalid Image Selected")

    def set_image(self, image: str) -> None:
        """
        Sets the preview image.
        :param image: Image to preview.
        """
        self._image = image
        self._set_label(image)
