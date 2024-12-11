import logging
import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QLabel, \
    QListWidget, QPushButton, \
    QWidget, QStackedLayout, QListWidgetItem, QSizePolicy, QDialog, QFormLayout, QLineEdit, \
    QMessageBox
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QDragLeaveEvent
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

# Default constants for plot settings
DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1080
DEFAULT_DPI = 200
DEFAULT_X_LABEL = "X Axis"
DEFAULT_Y_LABEL = "Y Axis"
DEFAULT_TITLE = "Plot"

# Set up logging configuration
logger = logging.getLogger(__name__)


class DragDropWidget(QFrame):
    """Widget for drag-and-drop file or folder handling."""

    DEFAULT_MESSAGE = "Drag and drop a CSV file or folder here"

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
        """Handle the drag enter event."""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if self._are_valid_paths(urls):
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
        """Reset style when the drag leaves the widget."""
        self.setStyleSheet(self.default_style)
        self.message_label.setText(self.DEFAULT_MESSAGE)

    def dropEvent(self, event: QDropEvent):
        """Handle the drop event."""
        if event.mimeData().hasUrls():
            file_paths = [url.toLocalFile() for url in event.mimeData().urls()]
            csv_files = self._collect_csv_files(file_paths)

            if csv_files:
                choice = self._ask_batch_preference()

                if choice == "separate":
                    # Process files separately (single files)
                    self.load_files_callback(csv_files, batch=False)
                elif choice == "batch":
                    # Process files as a batch
                    self.load_files_callback(csv_files, batch=True)

            self.setStyleSheet(self.default_style)
            self.message_label.setText(self.DEFAULT_MESSAGE)

    @staticmethod
    def _are_valid_paths(urls):
        """Check if all URLs are valid CSV files or folders."""
        for url in urls:
            path = url.toLocalFile()
            if os.path.isdir(path):
                continue
            elif os.path.isfile(path) and path.lower().endswith('.csv'):
                continue
            else:
                return False
        return True

    @staticmethod
    def _collect_csv_files(paths):
        """Recursively collect all CSV files from given paths."""
        csv_files = []
        for path in paths:
            if os.path.isfile(path) and path.lower().endswith('.csv'):
                csv_files.append(path)
            elif os.path.isdir(path):
                for root, _, files in os.walk(path):
                    csv_files.extend(
                        os.path.join(root, file) for file in files if file.lower().endswith('.csv')
                    )
        return csv_files

    def _ask_batch_preference(self):
        """Prompt the user to choose between separate or batch processing."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Batch Processing")
        msg_box.setText("How would you like to process the files?")
        separate_button = msg_box.addButton("Store separately", QMessageBox.ButtonRole.AcceptRole)
        batch_button = msg_box.addButton("Batch measurement", QMessageBox.ButtonRole.ActionRole)
        msg_box.exec()

        if msg_box.clickedButton() == separate_button:
            return "separate"
        elif msg_box.clickedButton() == batch_button:
            return "batch"
        return None


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


class OsmoUI(QWidget):
    def __init__(self, osmo_controller):
        super().__init__()
        self.controller = osmo_controller

        # Main frame setup
        self.main_frame = QFrame(self)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(self.main_frame)
        self.setLayout(self.main_layout)

        # Drag-and-drop widget as the initial content
        self.drag_drop_widget = DragDropWidget(self.load_files)
        self.main_frame_layout = QStackedLayout(self.main_frame)
        self.main_frame_layout.addWidget(self.drag_drop_widget)

        # Create placeholders for main layout components
        self.left_layout = None
        self.right_layout = None
        self.figure = None
        self.canvas = None
        self.plugins_list = None
        self.elements_list = None
        self.export_button = None

    def setup_main_layout(self):
        """Set up the main application layout."""
        # Horizontal layout for the main frame
        horizontal_layout = QHBoxLayout()

        # Left vertical layout
        left_frame = QFrame(self.main_frame)
        self.left_layout = QVBoxLayout(left_frame)

        # Canvas setup
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding,
                                  QSizePolicy.Policy.Expanding)
        self.left_layout.addWidget(self.canvas)

        # Make the canvas expand to fit the layout by adding a stretch factor
        self.left_layout.setStretch(0, 1)

        # Export button
        self.export_button = QPushButton("Export", self)
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(self.open_export_dialog)
        self.left_layout.addWidget(self.export_button)

        # Add left frame to the horizontal layout and set its stretch factor
        horizontal_layout.addWidget(left_frame,
                                    stretch=1)  # Set stretch factor to 1 for expansion

        # Right vertical layout
        right_frame = QFrame(self.main_frame)
        self.right_layout = QVBoxLayout(right_frame)

        # Plugins list
        plugins_label = QLabel("Plugins", self)
        self.right_layout.addWidget(plugins_label)

        self.plugins_list = QListWidget(self)
        self.plugins_list.itemChanged.connect(self.on_plugin_selection_changed)
        self.right_layout.addWidget(self.plugins_list)

        # Refresh Plugins button
        refresh_button = QPushButton("Refresh Plugins", self)
        refresh_button.clicked.connect(self.update_plugin_list)
        self.right_layout.addWidget(refresh_button)

        # Elements list
        elements_label = QLabel("Elements", self)
        self.right_layout.addWidget(elements_label)

        self.elements_list = QListWidget(self)
        self.elements_list.itemChanged.connect(
            self.on_element_selection_changed)
        self.right_layout.addWidget(self.elements_list)

        # Add right frame to the horizontal layout with a fixed size
        horizontal_layout.addWidget(right_frame)

        # Replace drag-and-drop widget with the main layout
        main_widget = QWidget()
        main_widget.setLayout(horizontal_layout)
        self.main_frame_layout.addWidget(main_widget)
        self.main_frame_layout.setCurrentWidget(main_widget)

    def load_files(self, file_paths, batch=False):
        """Handles file loading based on batch or single file processing."""
        if self.controller.load_files(file_paths, batch=batch):
            self.setup_main_layout()
            self.update_plugin_list()
            self.update_elements_list()
        else:
            logger.error("Error loading files.")

    def update_canvas(self):
        """Update the canvas with selected elements."""
        if self.figure:
            # Get the list of selected element IDs
            selected_element_ids = [
                self.elements_list.item(index).data(Qt.ItemDataRole.UserRole)
                for index in range(self.elements_list.count())
                if self.elements_list.item(
                    index).checkState() == Qt.CheckState.Checked
            ]

            # Update the figure by asking the controller for the updated canvas
            self.figure = self.controller.get_updated_canvas(
                selected_element_ids)
            self.canvas.figure = self.figure
            self.canvas.draw()

            # Enable the export button if there's visible data
            self.export_button.setEnabled(
                any(ax.has_data() for ax in self.figure.axes))

    def update_plugin_list(self):
        """Update the plugin list with checkboxes."""
        plugins = self.controller.get_plugins()
        self.plugins_list.clear()

        for plugin in plugins:
            item = QListWidgetItem(plugin["name"])
            item.setData(Qt.ItemDataRole.UserRole,
                         plugin["id"])  # Store plugin ID for future use
            item.setFlags(
                item.flags() | Qt.ItemFlag.ItemIsUserCheckable)  # Enable clickable
            item.setCheckState(
                Qt.CheckState.Unchecked)  # Default state is unchecked
            self.plugins_list.addItem(item)

    def update_elements_list(self):
        """Update the elements list to reflect the current state."""
        self.elements_list.clear()
        elements = self.controller.get_all_elements()

        for element_id, element in elements.items():
            item = QListWidgetItem(f"{element.label}, {element.plugin_name}")
            item.setData(Qt.ItemDataRole.UserRole,
                         element_id)  # Store the element ID
            if element.selected:
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)
            self.elements_list.addItem(item)

    def on_plugin_selection_changed(self, item):
        """Handles the selection change in the plugin list."""
        plugin_id = item.data(Qt.ItemDataRole.UserRole)  # Get the plugin ID

        if item.checkState() == Qt.CheckState.Checked:
            # Run the plugin and update the elements
            self.controller.run_plugin([plugin_id])
            self.update_elements_list()
            self.update_canvas()  # Redraw canvas with new elements
        else:
            # Remove plugin elements
            self.controller.remove_elements_by_plugin_id(
                plugin_id)
            self.update_elements_list()
            self.update_canvas()  # Redraw canvas without elements of the deselected plugin

    def on_element_selection_changed(self, item):
        """Handles the selection change in the elements list."""
        element_id = item.data(Qt.ItemDataRole.UserRole)

        if item.checkState() == Qt.CheckState.Checked:
            # Element selected
            logger.info(f"Element {element_id} selected.")
        else:
            # Element deselected
            logger.info(f"Element {element_id} deselected.")

        self.update_canvas()

    def open_export_dialog(self):
        """Open the export settings dialog."""
        dialog = ExportDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            settings = dialog.get_settings()
            if settings is None:
                # Log and return if validation failed in the dialog
                logger.warning("Export settings validation failed. Dialog remains open.")
                return

            filename = settings["filename"]
            if filename:
                try:
                    # Call the PlotManager's save_plot method
                    self.controller.save_plot(
                        filename, settings["width"], settings["height"],
                        settings["dpi"], settings["x_label"],
                        settings["y_label"], settings["title"]
                    )
                    QMessageBox.information(self, "Export Successful", f"Plot saved as {filename}")
                    dialog.accept()  # Close the dialog after successful export
                except Exception as e:
                    logger.error(f"Failed to save plot: {e}")
                    QMessageBox.critical(self, "Export Error",
                                         "An error occurred while saving the plot.")
            else:
                QMessageBox.warning(self, "Filename is missing", "Please name your file")
