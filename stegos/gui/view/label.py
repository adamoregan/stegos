from PySide6.QtCore import QEvent, QTimer, Qt
from PySide6.QtGui import QIcon, QResizeEvent, QPixmap
from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout, QStyle


class IconLabel(QLabel):
    """Label that shows an icon that automatically changes based on the current application theme."""

    def __init__(
        self,
        icon: QIcon.ThemeIcon,
        pixel_metric: QStyle.PixelMetric = QStyle.PixelMetric.PM_SmallIconSize,
    ):
        """
        Creates an instance of IconLabel.
        :param icon: Icon of the label.
        :param pixel_metric: Size of the icon.
        """
        super().__init__()
        self._icon = icon
        self._pixel_metric = pixel_metric
        self._set_pixmap()

    def _set_pixmap(self) -> None:
        """Sets the pixmap of the label based on the current application theme."""
        size = self.style().pixelMetric(self._pixel_metric)
        icon = QIcon.fromTheme(self._icon)
        self.setPixmap(icon.pixmap(size, size))

    def changeEvent(self, event: QEvent) -> None:
        """
        Handles Qt change events.

        Label icon changes when the application's theme changes.
        :param event: Event that occurred.
        """
        super().changeEvent(event)
        if event.type() == QEvent.Type.PaletteChange:
            QTimer.singleShot(0, self._set_pixmap)


class ErrorLabel(QWidget):
    """Label with text and an error icon."""

    def __init__(self, text: str = ""):
        """
        Creates an instance of ErrorLabel.
        :param text: Text to set the label to.
        """
        super().__init__(visible=False)
        self._icon_label = IconLabel(QIcon.ThemeIcon.DialogError)
        self._text_label = QLabel(text)
        self._text_label.setProperty("class", "error")
        self._create_layout()

    def _create_layout(self) -> None:
        """Creates the UI of the error label."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        layout.addWidget(self._icon_label)
        layout.addWidget(self._text_label)
        layout.addStretch()

    @property
    def text(self) -> str:
        """
        Gets the label text.
        :return: Label text.
        """
        return self._text_label.text()

    def set_text(self, text: str) -> None:
        """
        Sets the label text.
        :param text: Text to set the label to.
        """
        self._text_label.setText(text)


class ScaledPixmapLabel(QLabel):
    """Label with automatically scaling pixmap."""

    def __init__(self, *args, **kwargs):
        """Creates an instance of ScaledPixmapLabel."""
        super().__init__(*args, **kwargs)
        self._pixmap = QPixmap(self.pixmap())
        self.setMinimumSize(5, 5)  # allows pixmap to shrink

    def setPixmap(self, pixmap: QPixmap) -> None:
        """
        Sets the pixmap of the label.
        :param pixmap: Pixmap to set the label to.
        """
        self._pixmap = pixmap
        self._scale_pixmap()

    def _scale_pixmap(self) -> None:
        """Scales the pixmap depending on the size of the label."""
        if self._pixmap:
            scaled = self._pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            super().setPixmap(scaled)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Scales the pixmap automatically when the size of the label changes."""
        super().resizeEvent(event)
        self._scale_pixmap()


class BoldLabel(QLabel):
    """Label with bold text."""

    def __init__(self, *args, **kwargs):
        """Creates an instance of BoldLabel."""
        super().__init__(*args, **kwargs)
        font = self.font()
        font.setBold(True)
        self.setFont(font)
