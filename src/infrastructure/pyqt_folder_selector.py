from PyQt6.QtWidgets import QFileDialog
from src.core.interfaces.folder_selector import FolderSelector


class PyQtFolderSelector(FolderSelector):
    def select_folder(self) -> str:
        """Open a folder selection dialog and return the selected folder path."""
        folder = QFileDialog.getExistingDirectory(None, "Select Folder")
        return folder
