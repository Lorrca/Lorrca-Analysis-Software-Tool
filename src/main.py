import sys

from PySide6.QtWidgets import QApplication

from src.controllers.main_controller import MainController
from src.ui.main_ui import MainWindow


def main():
    app = QApplication(sys.argv)

    # Initialize the Main View and Controller
    controller = MainController()
    window = MainWindow(controller)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
