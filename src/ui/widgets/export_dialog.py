from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1080
DEFAULT_DPI = 200
DEFAULT_X_LABEL = "X Axis"
DEFAULT_Y_LABEL = "Y Axis"
DEFAULT_TITLE = "Plot"


class ExportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Export Plot Settings")
        self.layout = QFormLayout(self)

        # Add form fields for export settings
        self.filename_input = QLineEdit(self)
        self.layout.addRow("Filename:", self.filename_input)

        self.width_input = QLineEdit(str(DEFAULT_WIDTH), self)
        self.layout.addRow("Width (pixels):", self.width_input)

        self.height_input = QLineEdit(str(DEFAULT_HEIGHT), self)
        self.layout.addRow("Height (pixels):", self.height_input)

        self.dpi_input = QLineEdit(str(DEFAULT_DPI), self)
        self.layout.addRow("DPI:", self.dpi_input)

        self.x_label_input = QLineEdit(DEFAULT_X_LABEL, self)
        self.layout.addRow("X Label:", self.x_label_input)

        self.y_label_input = QLineEdit(DEFAULT_Y_LABEL, self)
        self.layout.addRow("Y Label:", self.y_label_input)

        self.title_input = QLineEdit(DEFAULT_TITLE, self)
        self.layout.addRow("Title (required):", self.title_input)

        # Add buttons
        self.buttons_layout = QVBoxLayout()
        self.export_button = QPushButton("Export", self)
        self.export_button.clicked.connect(self.accept)
        self.buttons_layout.addWidget(self.export_button)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)
        self.buttons_layout.addWidget(self.cancel_button)

        self.layout.addRow(self.buttons_layout)

    def get_settings(self):
        """Return the input data as a dictionary."""
        # Validate required fields
        if not self.title_input.text().strip():
            QMessageBox.critical(self, "Error", "Title is required.")
            return None

        # Validate that width, height, and dpi are integers
        try:
            width = int(self.width_input.text().strip())
            height = int(self.height_input.text().strip())
            dpi = int(self.dpi_input.text().strip())
        except ValueError:
            QMessageBox.critical(self, "Error", "Width, Height, and DPI must be valid integers.")
            return None

        return {
            "filename": self.filename_input.text().strip(),
            "width": width,
            "height": height,
            "dpi": dpi,
            "x_label": self.x_label_input.text().strip(),
            "y_label": self.y_label_input.text().strip(),
            "title": self.title_input.text().strip()
        }
