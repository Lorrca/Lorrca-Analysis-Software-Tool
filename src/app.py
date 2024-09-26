import sys
from PyQt6.QtWidgets import QApplication

from src.core.usecases.folder_selection_usecase import FolderSelectionUseCase
from infrastructure import PyQtFolderSelector
from presenters import FolderSelectionPresenter
from ui import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create instances of the necessary components
    folder_selector = PyQtFolderSelector()
    folder_selection_use_case = FolderSelectionUseCase(folder_selector)
    main_window = MainWindow()
    presenter = FolderSelectionPresenter(main_window, folder_selection_use_case)

    # Pass presenter to the view
    main_window.set_presenter(presenter)

    # Show the main window
    main_window.show()

    sys.exit(app.exec())
