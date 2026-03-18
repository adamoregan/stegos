from PySide6.QtCore import QFile, QTextStream


def read_resource(path: str) -> str:
    """
    Reads the content of a Qt resource.
    :param path: Path of the Qt resource.
    :return: Resource contents.
    """
    content = ""
    file = QFile(path)
    if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        stream = QTextStream(file)
        content = stream.readAll()
        file.close()
    return content
