from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QDragLeaveEvent

from src.utils.file_reader_helper import FileHelper as Helper


class DragDropWidget(QFrame):
    """Widget for drag-and-drop file or folder handling."""

    DEFAULT_MESSAGE = "Drag and drop a single or multiple measurement files here to start the analysis."

    def __init__(self, load_files_callback):
        super().__init__()
        self.load_files_callback = load_files_callback

        self.setAcceptDrops(True)

        self.default_style = """
            background-color: lightgray;
            border: 2px dashed gray;
            border-radius: 10px;
        """
        self.valid_style = """
            background-color: lightblue;
            border: 2px dashed blue;
            border-radius: 10px;
        """
        self.invalid_style = """
            background-color: lightcoral;
            border: 2px dashed red;
            border-radius: 10px;
        """

        self.setStyleSheet(self.default_style)

        layout = QVBoxLayout(self)
        self.message_label = QLabel(self.DEFAULT_MESSAGE, self)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.message_label)
        self.setLayout(layout)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if Helper.are_valid_paths(urls):
                event.acceptProposedAction()
                self.setStyleSheet(self.valid_style)
                self.message_label.setText("Release to load CSV file(s) or folder(s)")
            else:
                event.acceptProposedAction()
                self.setStyleSheet(self.invalid_style)
                self.message_label.setText("Unsupported file type. Only CSV files are allowed.")
        else:
            event.ignore()

    def dragLeaveEvent(self, event: QDragLeaveEvent):
        self.setStyleSheet(self.default_style)
        self.message_label.setText(self.DEFAULT_MESSAGE)

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            file_paths = [url.toLocalFile() for url in event.mimeData().urls()]
            csv_files = Helper.collect_csv_files(file_paths)

            if csv_files:
                self.load_files_callback(csv_files)

            self.setStyleSheet(self.default_style)
            self.message_label.setText(self.DEFAULT_MESSAGE)


