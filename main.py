import sys

from stegos.gui.app import SteganographyApplication, MainWindow

if __name__ == "__main__":
    app = SteganographyApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
