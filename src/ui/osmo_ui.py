import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QLabel, \
    QListWidget, QPushButton, \
    QWidget, QStackedLayout, QListWidgetItem, QSizePolicy
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

# Set up logging configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DragDropWidget(QFrame):
    """Widget for drag-and-drop file handling."""

    def __init__(self, file_loaded_callback):
        super().__init__()
        self.file_loaded_callback = file_loaded_callback
        self.setAcceptDrops(True)
        self.setStyleSheet(
            "background-color: lightgray; border: 2px dashed gray;")
        layout = QVBoxLayout(self)
        label = QLabel("Drag and drop a file here", self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path:
                self.file_loaded_callback(file_path)


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
        self.drag_drop_widget = DragDropWidget(self.file_loaded)
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

    def file_loaded(self, file_path):
        """Handle file loading and initialize the main layout."""
        logger.info(f"File loaded: {file_path}")
        if self.controller.load_file(file_path):
            self.setup_main_layout()
            self.update_plugin_list()
            self.update_elements_list()

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
            item.setCheckState(
                Qt.CheckState.Checked)  # Set initial state as selected
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
