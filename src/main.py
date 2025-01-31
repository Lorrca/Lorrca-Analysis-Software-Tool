import sys

from PySide6.QtWidgets import QApplication

from src.ui.main_ui import MainWindow


def main():
    app = QApplication(sys.argv)

    # Initialize the Main View and Controller
    window = MainWindow()

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
