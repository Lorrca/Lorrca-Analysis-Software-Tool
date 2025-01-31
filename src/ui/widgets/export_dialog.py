from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, \
    QMessageBox, QCheckBox

DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1080
DEFAULT_DPI = 200
DEFAULT_X_LABEL = "X Axis"
DEFAULT_Y_LABEL = "Y Axis"
DEFAULT_TITLE = "Plot"


class ExportDialog(QDialog):
    def __init__(self, parent=None, x_label=DEFAULT_X_LABEL, y_label=DEFAULT_Y_LABEL,
                 title=DEFAULT_TITLE):
        super().__init__(parent)
        self.setWindowTitle("Export Plot Settings")
        self.layout = QFormLayout(self)

        # Add form fields for export settings
        self.filename_input = QLineEdit(title, self)  # Set to title as default value
        self.layout.addRow("Filename (required):", self.filename_input)

        self.width_input = QLineEdit(str(DEFAULT_WIDTH), self)
        self.layout.addRow("Width (pixels):", self.width_input)

        self.height_input = QLineEdit(str(DEFAULT_HEIGHT), self)
        self.layout.addRow("Height (pixels):", self.height_input)

        self.dpi_input = QLineEdit(str(DEFAULT_DPI), self)
        self.layout.addRow("DPI:", self.dpi_input)

        # Pre-fill the axis labels and title fields, fall back to defaults if not provided
        self.x_label_input = QLineEdit(x_label, self)
        self.layout.addRow("X Label:", self.x_label_input)

        self.y_label_input = QLineEdit(y_label, self)
        self.layout.addRow("Y Label:", self.y_label_input)

        self.title_input = QLineEdit(title, self)
        self.layout.addRow("Title:", self.title_input)

        # Grid checkbox (default: checked)
        self.grid_checkbox = QCheckBox("Enable Grid", self)
        self.grid_checkbox.setChecked(True)
        self.layout.addRow(self.grid_checkbox)

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
        """Return the input data as a dictionary with defaults as fallbacks."""
        # Validate that width, height, and dpi are integers
        try:
            width = int(
                self.width_input.text().strip()) if self.width_input.text().strip() else DEFAULT_WIDTH
            height = int(
                self.height_input.text().strip()) if self.height_input.text().strip() else DEFAULT_HEIGHT
            dpi = int(
                self.dpi_input.text().strip()) if self.dpi_input.text().strip() else DEFAULT_DPI
        except ValueError:
            QMessageBox.critical(self, "Error", "Width, Height, and DPI must be valid integers.")
            return None

        # Use defaults if optional fields are empty
        filename = self.filename_input.text().strip() or DEFAULT_TITLE
        x_label = self.x_label_input.text().strip() or DEFAULT_X_LABEL
        y_label = self.y_label_input.text().strip() or DEFAULT_Y_LABEL
        title = self.title_input.text().strip() or DEFAULT_TITLE
        grid_enabled = self.grid_checkbox.isChecked()

        return {
            "filename": filename,
            "width": width,
            "height": height,
            "dpi": dpi,
            "x_label": x_label,
            "y_label": y_label,
            "title": title,
            "grid": grid_enabled
        }
