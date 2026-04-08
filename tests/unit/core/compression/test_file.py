import io
import zipfile

import pytest

from stegos.core.compression.file import ZipCompressor


@pytest.fixture
def compressor():
    return ZipCompressor()


class TestZipCompressor:
    """Tests for ZipCompressor."""

    def test_compress_is_zip(self, compressor, tmp_path):
        """Compression should result in a zip file."""
        file = tmp_path / "file"
        file.write_bytes(b"File Content")
        compressed = compressor.compress(file)
        assert zipfile.is_zipfile(io.BytesIO(compressed))

    def test_compress_decompress(self, compressor, tmp_path):
        """Compressing and decompressing should maintain file integrity."""
        file_content = b"File Content"
        file = tmp_path / "file"

        file.write_bytes(file_content)

        compressed = compressor.compress(file)
        for filename, content in compressor.decompress(compressed):
            assert content == file_content

    def test_compress_decompress_multiple(self, compressor, tmp_path):
        """Compressing and decompressing should maintain file integrity for multiple files."""
        file_content = b"File Content"
        file1, file2 = tmp_path / "file1", tmp_path / "file2"

        file1.write_bytes(file_content)
        file2.write_bytes(file_content)

        compressed = compressor.compress([file1, file2])
        for filename, content in compressor.decompress(compressed):
            assert content == file_content

    def test_compress_decompress_basenames(self, compressor, tmp_path):
        """Compressing and decompressing should only use the basenames of given paths."""
        file = tmp_path / "file"

        file.write_bytes(b"File Content")

        compressed = compressor.compress(file)
        for filename, content in compressor.decompress(compressed):
            assert file.name.endswith(filename)

    def test_compress_decompress_duplicates(self, compressor, tmp_path):
        """Compressing and decompressing should not overwrite files with the same name but different paths."""
        file_name = "file"
        file_content = b"File Content"
        file_content2 = file_content + b" (Duplicated)"
        file1 = tmp_path / file_name
        file2 = tmp_path / "dir" / file_name

        file1.write_bytes(file_content)
        file2.parent.mkdir()
        file2.write_bytes(file_content2)

        compressed = compressor.compress([file1, file2])
        contents = [content for _, content in compressor.decompress(compressed)]
        assert contents == [file_content, file_content2]
