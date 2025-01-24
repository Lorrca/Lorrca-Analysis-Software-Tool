import logging

from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QWidget, QFrame, QHBoxLayout, QStackedLayout, QVBoxLayout, \
    QPushButton, QToolButton, QLabel, QTreeView, QDialog, QMessageBox, QTreeWidgetItem
from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from src.ui.widgets.drag_drop_widget import DragDropWidget
from src.ui.widgets.export_dialog import ExportDialog
from src.ui.widgets.measurement_tree_widget import MeasurementTreeWidget
from src.utils.file_reader_helper import FileHelper

logger = logging.getLogger(__name__)


class MeasurementUI(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.controller.register_view(self)

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
        self.export_button = None
        self.toolbar = None
        self.tree = None

    def setup_main_layout(self):
        horizontal_layout = QHBoxLayout()

        # Left Frame (Canvas and Export Button)
        left_frame = QFrame(self.main_frame)
        self.left_layout = QVBoxLayout(left_frame)

        # Create the canvas for the plot
        self.canvas = FigureCanvas(
            self.controller.get_updated_canvas([]))  # Initialize with an empty canvas

        # Create a navigation toolbar for interactivity (zoom, pan, etc.)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        # Add the toolbar and canvas to the layout
        self.left_layout.addWidget(self.toolbar)
        self.left_layout.addWidget(self.canvas)

        # Add export button with help icon
        export_layout = QHBoxLayout()

        self.export_button = QPushButton("Advanced Export", self)
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(self.open_export_dialog)
        export_layout.addWidget(self.export_button)

        export_help_button = QToolButton(self)
        export_help_button.setIcon(QIcon.fromTheme("help-about"))  # Standard "info" icon
        export_help_button.setToolTip(
            "A flexible way to export the plot. <br>"
            "The exported image will be stored in the designated 'results' folder in the root."
        )  # Help text with line break
        export_help_button.setCursor(Qt.CursorShape.PointingHandCursor)  # Make it feel clickable
        export_layout.addWidget(export_help_button)

        self.left_layout.addLayout(export_layout)

        horizontal_layout.addWidget(left_frame, stretch=1)

        # Right Frame (TreeView for Measurements and Elements)
        right_frame = QFrame(self.main_frame)
        self.right_layout = QVBoxLayout(right_frame)

        # Add "Measurements" label with an "i" icon
        measurements_label_layout = QHBoxLayout()
        measurements_label = QLabel("Measurements", self)
        measurements_label_layout.addWidget(measurements_label)

        help_button = QToolButton(self)
        help_button.setIcon(QIcon.fromTheme("help-about"))  # Standard "info" icon
        help_button.setToolTip(
            "Select a measurement to analyze. <br>"
            "Plugins run on the selected measurement, creating elements for further analysis."
        )  # Help text
        help_button.setCursor(Qt.CursorShape.PointingHandCursor)  # Make it feel clickable

        measurements_label_layout.addWidget(help_button)
        measurements_label_layout.addStretch()  # Push everything to the left

        self.right_layout.addLayout(measurements_label_layout)

        # TreeView for displaying measurements and elements
        self.tree = MeasurementTreeWidget()
        self.tree.fileDropped.connect(self.on_files_dropped)
        self.tree.setHeaderHidden(True)  # Hide the header for simplicity
        self.tree.setSelectionMode(QTreeView.SelectionMode.MultiSelection)
        self.tree.setHeaderLabel("Measurement")

        self.right_layout.addWidget(self.tree)

        horizontal_layout.addWidget(right_frame)
        main_widget = QWidget()
        main_widget.setLayout(horizontal_layout)
        self.main_frame_layout.addWidget(main_widget)
        self.main_frame_layout.setCurrentWidget(main_widget)

    def load_files(self, file_paths):
        """Load files and delegate storage to the controller."""
        if self.controller.initial_file_load(file_paths):
            self.setup_main_layout()
            self.update_measurement_tree_widget()
        else:
            logger.error("Error loading files.")

    def update_canvas(self):
        # Collect selected element IDs (checked elements only)
        selected_elements_ids = []

        # Iterate through top-level items (measurements)
        for i in range(self.tree.topLevelItemCount()):
            measurement_item = self.tree.topLevelItem(i)

            # Iterate through child items (elements)
            for j in range(measurement_item.childCount()):
                element_item = measurement_item.child(j)

                # Check if the child item (element) is checked
                if element_item.checkState(0) == Qt.CheckState.Checked:
                    selected_elements_ids.append(element_item.data(0, Qt.ItemDataRole.UserRole))

        # Update the canvas with selected elements
        self.canvas.figure = self.controller.get_updated_canvas(selected_elements_ids)

        # Adjust canvas size based on the current widget size
        width, height = self.canvas.size().width(), self.canvas.size().height()
        self.canvas.figure.set_size_inches(width / 100, height / 100)  # Set figure size in inches

        # Enable export button if there is any plot data
        self.export_button.setEnabled(any(ax.has_data() for ax in self.canvas.figure.axes))

    def update_measurement_tree_widget(self):
        """
        Update the tree view with measurements and their elements, maintaining selection state.
        """
        self.tree.itemChanged.disconnect(self.on_item_changed)
        # Track the selected state before the update
        selected_elements_before_update = self._track_selected_elements()

        # Fetch all models with their selection state from the controller
        all_models_with_selection = self.controller.get_all_measurements_with_selection()

        # Update or create tree items for each model
        for model, is_selected in all_models_with_selection:
            model_item = self.find_item_by_model_id(model.id)

            if model_item:
                self._update_existing_model_item(model_item, model)
            else:
                model_item = self._create_new_model_item(model, is_selected)

            # Restore selection for the model item after it's updated
            self._restore_element_selection(model_item, model.id, selected_elements_before_update)

        # Refresh the canvas with the selected elements
        self.update_canvas()

        # Reconnect the itemChanged signal after updating the tree
        self.tree.itemChanged.connect(self.on_item_changed)

    def _track_selected_elements(self):
        """Return selected elements in the tree."""
        selected_elements = {}
        for i in range(self.tree.topLevelItemCount()):
            measurement_item = self.tree.topLevelItem(i)
            model_id = measurement_item.data(0, Qt.ItemDataRole.UserRole)
            for j in range(measurement_item.childCount()):
                element_item = measurement_item.child(j)
                if element_item.checkState(0) == Qt.CheckState.Checked:
                    selected_elements.setdefault(model_id, set()).add(
                        element_item.data(0, Qt.ItemDataRole.UserRole))
        return selected_elements

    def _update_or_create_model_item(self, model, is_selected, selected_elements_before_update):
        """Update an existing model item or create a new one."""
        model_item = self.find_item_by_model_id(model.id)

        if model_item:
            self._update_existing_model_item(model_item, model)
        else:
            self._create_new_model_item(model, is_selected)

    def _update_existing_model_item(self, model_item, model):
        """Update an existing model item and its elements."""
        # Preserve the selection state of the model
        model_selected = model_item.checkState(0) == Qt.CheckState.Checked

        # Clear current children (elements) for the model item
        model_item.takeChildren()

        # Add elements for the model from the controller
        self.add_elements_to_tree(model_item, model.id)

        # Restore the model's checkbox state
        model_item.setCheckState(0,
                                 Qt.CheckState.Checked if model_selected
                                 else Qt.CheckState.Unchecked)

    def _create_new_model_item(self, model, is_selected):
        """Create a new model item and add its elements."""
        model_item = QTreeWidgetItem([model.name])
        model_item.setData(0, Qt.ItemDataRole.UserRole, model.id)
        model_item.setFlags(model_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        self.tree.addTopLevelItem(model_item)

        # Add elements for the new model
        self.add_elements_to_tree(model_item, model.id)

        # Set initial checkbox state for the model
        model_item.setCheckState(0,
                                 Qt.CheckState.Checked if is_selected else Qt.CheckState.Unchecked)

        return model_item

    @staticmethod
    def _restore_element_selection(model_item, model_id, selected_elements_before_update):
        """Restore the selection state of elements for a model item."""
        selected_elements = selected_elements_before_update.get(model_id, set())
        for i in range(model_item.childCount()):
            element_item = model_item.child(i)
            element_id = element_item.data(0, Qt.ItemDataRole.UserRole)
            element_item.setCheckState(0,
                                       Qt.CheckState.Checked if element_id in selected_elements
                                       else Qt.CheckState.Unchecked)

    def find_item_by_model_id(self, model_id: str):
        """Helper function to find a tree item by model ID."""
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            if item.data(0, Qt.ItemDataRole.UserRole) == model_id:
                return item
        return None

    def on_item_changed(self, item, column):
        if column != 0:  # Only handle checkbox changes
            return

        model_id = item.data(0, Qt.ItemDataRole.UserRole)

        # Temporarily disconnect signal to avoid recursion during updates
        self.tree.itemChanged.disconnect(self.on_item_changed)

        if item.parent() is None:  # It's a measurement item
            # Update measurement selection
            is_selected = item.checkState(0) == Qt.CheckState.Checked
            self.controller.update_model_selection(model_id, is_selected)

            if is_selected:
                # Add elements to the tree if the model is selected
                self.add_elements_to_tree(item, model_id)
            else:
                # Remove child elements when the model is deselected
                item.takeChildren()

        # Update canvas after selection change
        self.update_canvas()

        # Reconnect the signal after handling the item change
        self.tree.itemChanged.connect(self.on_item_changed)

    def add_elements_to_tree(self, parent_item, model_id):
        elements = self.controller.get_elements_by_model_id(model_id)
        existing_element_ids = {child.data(0, Qt.ItemDataRole.UserRole) for child in
                                parent_item.takeChildren()}

        for element in elements:
            if element.id not in existing_element_ids:
                child_item = QTreeWidgetItem([f"{element.label} - {element.plugin_name}"])
                child_item.setData(0, Qt.ItemDataRole.UserRole, element.id)
                child_item.setFlags(child_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                child_item.setCheckState(0, Qt.CheckState.Unchecked)
                parent_item.addChild(child_item)

    def open_export_dialog(self):
        x_label, y_label, title = self.get_figure_labels()
        dialog = ExportDialog(self, x_label, y_label, title)

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

    def on_files_dropped(self, file_paths):
        """Handle files dropped onto the models list."""
        csv_files = FileHelper.collect_csv_files(file_paths)  # Collect valid CSV files
        if csv_files:
            logger.info(f"CSV Files Dropped: {csv_files}")
            self.controller.load_files(csv_files)  # Process dropped files
            self.update_measurement_tree_widget()  # Refresh model list after loading files
        else:
            logger.warning("No valid CSV files found.")  # Log invalid files

    def get_figure_labels(self):
        x_label = self.canvas.figure.axes[0].get_xlabel()
        y_label = self.canvas.figure.axes[0].get_ylabel()
        title = self.canvas.figure.axes[0].get_title()

        return x_label, y_label, title

    def cleanup(self):
        """Detach controller from the view."""
        self.controller = None
