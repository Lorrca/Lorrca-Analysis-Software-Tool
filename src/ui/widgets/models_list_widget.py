from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QListWidget, QMenu

from src.utils.file_reader_helper import FileHelper as Helper  # Import the Helper class


class ModelsListWidget(QListWidget):
    fileDropped = Signal(list)  # Signal to notify when files are dropped

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.default_style = ""  # Default background style

    def dragEnterEvent(self, event):
        file_urls = event.mimeData().urls()

        # Use Helper to check if the files are valid
        if Helper.are_valid_paths(file_urls):
            event.accept()
            self.setStyleSheet(
                "background-color: lightblue;")  # Show blue background for valid CSV files
        else:
            event.ignore()
            self.setStyleSheet(
                "background-color: lightcoral;")  # Show red background for invalid files

    def dragMoveEvent(self, event):
        file_urls = event.mimeData().urls()

        # Use Helper to check if the files are valid
        if Helper.are_valid_paths(file_urls):
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        # Reset background style when drag leaves the widget
        self.setStyleSheet(self.default_style)

    def dropEvent(self, event):
        file_urls = event.mimeData().urls()

        # Use Helper to check if the files are valid
        if Helper.are_valid_paths(file_urls):
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
            file_paths = [url.toLocalFile() for url in file_urls]
            self.fileDropped.emit(file_paths)  # Emit signal with file paths
            self.setStyleSheet(self.default_style)  # Reset background color after drop
        else:
            event.ignore()  # Ignore if files are not valid CSV
            self.setStyleSheet("background-color: lightcoral;")  # Show red for invalid files
