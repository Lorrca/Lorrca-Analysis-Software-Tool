import sys

from PySide6.QtWidgets import QMainWindow, QApplication

from main import Ui_MainWindow


class LoadMainWindow(QMainWindow):
    def __init__(self):
        super(LoadMainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = LoadMainWindow()
    ui.show()
    sys.exit(app.exec())