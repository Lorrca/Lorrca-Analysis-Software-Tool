import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QLabel, QListWidget, QPushButton, \
    QWidget, QStackedLayout, QListWidgetItem, QDialog, QMessageBox
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from src.ui.widgets.drag_drop_widget import DragDropWidget
from src.ui.widgets.export_dialog import ExportDialog
from src.ui.widgets.models_list_widget import ModelsListWidget

from src.utils.file_reader_helper import FileHelper as Helper

logger = logging.getLogger(__name__)


class MeasurementUI(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.main_frame = QFrame(self)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(self.main_frame)
        self.setLayout(self.main_layout)

        self.drag_drop_widget = DragDropWidget(self.load_files)  # Existing drag and drop widget
        self.main_frame_layout = QStackedLayout(self.main_frame)
        self.main_frame_layout.addWidget(self.drag_drop_widget)

        self.left_layout = None
        self.right_layout = None
        self.canvas = None
        self.models_list = None
        self.elements_list = None
        self.export_button = None

    def setup_main_layout(self):
        horizontal_layout = QHBoxLayout()

        left_frame = QFrame(self.main_frame)
        self.left_layout = QVBoxLayout(left_frame)
        self.canvas = FigureCanvas()

        self.left_layout.addWidget(self.canvas)

        self.export_button = QPushButton("Export", self)
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(self.open_export_dialog)
        self.left_layout.addWidget(self.export_button)
        horizontal_layout.addWidget(left_frame, stretch=1)

        right_frame = QFrame(self.main_frame)
        self.right_layout = QVBoxLayout(right_frame)

        models_label = QLabel("Models", self)
        self.right_layout.addWidget(models_label)

        # Use ModelsListWidget here
        self.models_list = ModelsListWidget(self)
        self.models_list.fileDropped.connect(self.on_files_dropped)  # Handle dropped files
        self.models_list.itemChanged.connect(
            self.on_model_selection_changed)  # Connect to item change
        self.right_layout.addWidget(self.models_list)

        elements_label = QLabel("Elements", self)
        self.right_layout.addWidget(elements_label)

        self.elements_list = QListWidget(self)
        self.elements_list.itemChanged.connect(self.update_canvas)
        self.right_layout.addWidget(self.elements_list)

        horizontal_layout.addWidget(right_frame)
        main_widget = QWidget()
        main_widget.setLayout(horizontal_layout)
        self.main_frame_layout.addWidget(main_widget)
        self.main_frame_layout.setCurrentWidget(main_widget)

    def load_files(self, file_paths):
        if self.controller.load_files(file_paths):
            self.setup_main_layout()
            self.update_model_list()
            self.update_elements_list()
        else:
            logger.error("Error loading files.")

    def update_canvas(self):
        selected_elements_ids = [
            self.elements_list.item(index).data(Qt.ItemDataRole.UserRole)
            for index in range(self.elements_list.count())
            if self.elements_list.item(index).checkState() == Qt.CheckState.Checked
        ]
        self.canvas.figure = self.controller.get_updated_canvas(selected_elements_ids)
        width, height = self.canvas.size().width(), self.canvas.size().height()
        self.canvas.figure.set_size_inches(width / 80, height / 80)
        self.canvas.draw()
        self.export_button.setEnabled(any(ax.has_data() for ax in self.canvas.figure.axes))

    def update_model_list(self):
        models = self.controller.get_all_models_with_selection()
        self.models_list.clear()

        for model_id, measurement_id, selected in models:
            item = QListWidgetItem(measurement_id)
            item.setData(Qt.ItemDataRole.UserRole, model_id)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked if selected else Qt.CheckState.Unchecked)
            self.models_list.addItem(item)

    def update_elements_list(self):
        # Store current selection states in a dictionary
        current_selections = {
            self.elements_list.item(index).data(Qt.ItemDataRole.UserRole):
                self.elements_list.item(index).checkState() == Qt.CheckState.Checked
            for index in range(self.elements_list.count())
        }

        # Clear the list
        elements = self.controller.get_all_elements()
        self.elements_list.clear()

        # Create a list of tuples with element data (ID, label, plugin_name, model_name)
        element_data = [
            (element_id, element.label, element.plugin.plugin_name, element.model.name)
            for element_id, element in elements.items()
        ]

        # Rebuild the list and reapply previous selections
        for element_id, label, plugin_name, model_name in element_data:
            item = QListWidgetItem(f"| {label} | Plugin: {plugin_name} | Model: {model_name} |")
            item.setData(Qt.ItemDataRole.UserRole, element_id)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            # Apply the stored selection state or default to unchecked
            item.setCheckState(
                Qt.CheckState.Checked if current_selections.get(element_id,
                                                                False) else Qt.CheckState.Unchecked
            )
            self.elements_list.addItem(item)

    def on_model_selection_changed(self, item):
        """Handle model selection changes."""
        model_id = item.data(Qt.ItemDataRole.UserRole)
        checked = item.checkState() == Qt.CheckState.Checked
        self.controller.update_model_selection(model_id, checked)
        self.update_elements_list()
        self.update_canvas()

    def on_files_dropped(self, file_paths):
        """Handle files dropped onto the models list."""
        csv_files = Helper.collect_csv_files(file_paths)  # Collect valid CSV files
        if csv_files:
            print("CSV Files Dropped:", csv_files)
            self.controller.load_files(csv_files)  # Process dropped files
            self.update_model_list()  # Refresh model list after loading files
        else:
            print("No valid CSV files found.")  # Log invalid files

    def open_export_dialog(self):
        dialog = ExportDialog(self)
        while True:
            if dialog.exec() == QDialog.DialogCode.Accepted:
                settings = dialog.get_settings()
                if settings is None:
                    logger.warning("Export settings validation failed. Dialog remains open.")
                    continue
                filename = settings.get("filename", "")
                if filename:
                    try:
                        self.controller.save_plot(
                            filename, settings["width"], settings["height"],
                            settings["dpi"], settings["x_label"],
                            settings["y_label"], settings["title"]
                        )
                        QMessageBox.information(self, "Export Successful",
                                                f"Plot saved as {filename}")
                        dialog.accept()
                        break
                    except Exception as e:
                        logger.error(f"Failed to save plot: {e}")
                        QMessageBox.critical(self, "Export Error",
                                             f"An error occurred while saving the plot: {e}")
                else:
                    QMessageBox.warning(self, "Filename is missing", "Please name your file")
            else:
                break

    def cleanup(self):
        """Detach controller from the view."""
        self.controller = None
