import sys
from PyQt6.QtWidgets import QApplication

from src.core.usecases.folder_selection_usecase import FolderSelectionUseCase
from src.infrastructure.pyqt_folder_selector import PyQtFolderSelector
from src.presenters.folder_selection_presenter import FolderSelectionPresenter
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create instances of the necessary components
    folder_selector = PyQtFolderSelector()
    folder_selection_use_case = FolderSelectionUseCase(folder_selector)
    presenter = FolderSelectionPresenter(None, folder_selection_use_case)  # Initialize with None first

    main_window = MainWindow(presenter)  # Pass presenter to MainWindow
    presenter.view = main_window  # Set the view in the presenter

    # Show the main window
    main_window.show()

    sys.exit(app.exec())
