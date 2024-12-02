from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QLabel, QListWidget, QPushButton, \
    QWidget, QStackedLayout, QListWidgetItem
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class DragDropWidget(QFrame):
    """Widget for drag-and-drop file handling."""

    def __init__(self, file_loaded_callback):
        super().__init__()
        self.file_loaded_callback = file_loaded_callback
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: lightgray; border: 2px dashed gray;")
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
        # Horizontal layout for main frame
        horizontal_layout = QHBoxLayout()

        # Left vertical layout
        left_frame = QFrame(self.main_frame)
        self.left_layout = QVBoxLayout(left_frame)

        # Canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.left_layout.addWidget(self.canvas)

        # Export button
        self.export_button = QPushButton("Export", self)
        self.export_button.setEnabled(False)
        self.left_layout.addWidget(self.export_button)

        horizontal_layout.addWidget(left_frame)

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
        self.right_layout.addWidget(self.elements_list)

        horizontal_layout.addWidget(right_frame)

        # Replace drag-and-drop widget with the main layout
        main_widget = QWidget()
        main_widget.setLayout(horizontal_layout)
        self.main_frame_layout.addWidget(main_widget)
        self.main_frame_layout.setCurrentWidget(main_widget)

    def file_loaded(self, file_path):
        """Handle file loading and initialize the main layout."""
        print(f"File loaded: {file_path}")
        if self.controller.load_file(file_path):  # Assume controller processes the file
            self.setup_main_layout()
            self.update_plugin_list()
            self.update_canvas()

    def update_canvas(self):
        """Update the canvas with a new figure."""
        if self.figure:
            self.figure = self.controller.get_figure()
            self.canvas.figure = self.figure
            self.canvas.draw()

            # Enable the export button if there's visible data
            self.export_button.setEnabled(
                any(ax.has_data() for ax in self.figure.axes)
            )

    def update_plugin_list(self):
        """Update the plugin list with checkboxes."""
        plugins = self.controller.get_plugins()
        self.plugins_list.clear()

        for plugin in plugins:
            item = QListWidgetItem(plugin["name"])
            item.setData(Qt.UserRole, plugin["id"])  # Store plugin ID for future use
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)  # Enable checkable
            item.setCheckState(Qt.CheckState.Unchecked)  # Default state is unchecked
            self.plugins_list.addItem(item)

    def get_checked_plugins(self):
        """Get a list of checked plugins by their IDs."""
        checked_plugins = []
        for index in range(self.plugins_list.count()):
            item = self.plugins_list.item(index)
            if item.checkState() == Qt.CheckState.Checked:
                plugin_id = item.data(Qt.UserRole)
                checked_plugins.append(plugin_id)
        return checked_plugins

    def on_plugin_selection_changed(self, item):
        """Handles the selection change in the plugin list."""
        # Get the plugin ID from the item data
        plugin_id = item.data(Qt.UserRole)

        # Check if the plugin is selected or deselected
        if item.checkState() == Qt.CheckState.Checked:
            # Run the selected plugin
            self.controller.run_plugin(
                [plugin_id])  # Pass the list of selected plugin IDs (even if it's just one)
