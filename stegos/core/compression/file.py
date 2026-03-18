import io
import os
import zipfile
from abc import ABC, abstractmethod
from typing import Iterable, Generator


class FileCompressor(ABC):
    """Compressor for compressing and decompressing files in memory."""

    @abstractmethod
    def compress(self, files: str | os.PathLike[str] | Iterable[str]) -> bytes:
        """
        Compresses files.
        :param files: Files to compress.
        :return: Bytes archive of compressed files.
        """
        pass

    @abstractmethod
    def decompress(self, archive: bytes) -> Generator[tuple[str, bytes], None, None]:
        """
        Decompresses files.
        :param archive: Bytes archive of compressed files.
        :return: Name and content for each file.
        """
        pass


class ZipCompressor(FileCompressor):
    """Compressor for compressing and decompressing files using the ZIP format."""

    def __init__(self, compression: int = zipfile.ZIP_DEFLATED):
        self._compression = compression

    def compress(self, files):
        if isinstance(files, (str, os.PathLike)):
            files = [files]

        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", self._compression) as zf:
            for file in files:
                zf.write(file, arcname=os.path.basename(file))

        return buffer.getvalue()

    def decompress(self, zip_file):
        with zipfile.ZipFile(io.BytesIO(zip_file), "r") as zf:
            for (
                file
            ) in zf.infolist():  # allows files to be gotten that have duplicate names
                with zf.open(file) as f:
                    yield file.filename, f.read()
