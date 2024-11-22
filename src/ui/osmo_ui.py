from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QFrame, QVBoxLayout, QLabel, QListWidget, QPushButton, \
    QListWidgetItem, QWidget
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class OsmoUI(QWidget):
    def __init__(self, osmo_controller):
        super().__init__()
        self.plot_layout = None
        print(f"OsmoUI {self} created")

        self.controller = osmo_controller
        self.elements_list = None
        self.elements_label = None
        self.refresh_plugins_button = None
        self.plugins_list = None
        self.plugins_label = None
        self.export_button = None
        self.data_frame = None

        # Initialize an empty figure for the canvas
        self.figure = Figure()  # Empty figure
        self.canvas = FigureCanvas(self.figure)  # Canvas based on the empty figure

        # Set up the layout
        self.setup_layout()

        # Populate the plugin list on initialization
        self.update_plugin_list()

    def setup_layout(self):
        """Set up the main layout and widgets."""
        main_layout = QHBoxLayout(self)

        # Left Frame
        self.data_frame = QFrame(self)
        main_layout.addWidget(self.data_frame)

        # Right Layout (Plugins and Elements)
        right_layout = QVBoxLayout()

        # Plugin List Section
        self.setup_plugin_list_section(right_layout)

        # Elements List Section
        self.setup_elements_list_section(right_layout)

        # Plot Widget
        self.setup_plot_widget()

        # Add the right layout to the main layout
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

    def setup_plugin_list_section(self, layout):
        """Set up the plugin list section."""
        self.plugins_label = QLabel("Plugins", self)
        layout.addWidget(self.plugins_label)

        # Plugins List Widget
        self.plugins_list = QListWidget(self)
        layout.addWidget(self.plugins_list)

        # Refresh Plugins Button
        self.refresh_plugins_button = QPushButton("Refresh Plugins", self)
        self.refresh_plugins_button.clicked.connect(self.update_plugin_list)
        layout.addWidget(self.refresh_plugins_button)

    def setup_elements_list_section(self, layout):
        """Set up the elements list section."""
        self.elements_label = QLabel("Elements", self)
        layout.addWidget(self.elements_label)

        # Elements List Widget
        self.elements_list = QListWidget(self)
        layout.addWidget(self.elements_list)

    def setup_plot_widget(self):
        """Set up the plot section with a canvas and export button."""
        plot_frame = QFrame(self)
        plot_layout = QVBoxLayout(plot_frame)

        # Add the canvas to the layout
        plot_layout.addWidget(self.canvas)

        # Export Button
        self.export_button = QPushButton("Export", self)
        self.export_button.setEnabled(False)  # Initially disabled
        plot_layout.addWidget(self.export_button)

        # Store the layout for future updates
        self.plot_layout = plot_layout

        self.layout().addWidget(plot_frame)

    def update_canvas(self):
        """Update the canvas with a new figure or redraw the existing one."""
        self.figure = self.controller.get_figure()
        if self.figure:
            self.canvas.figure = self.figure  # Replace the figure
        self.canvas.draw()  # Redraw the canvas

        # Check if the figure contains any visible data (axes or content)
        is_plot_displayed = any(
            ax.has_data() for ax in self.canvas.figure.axes  # Check if axes have any data
        )
        self.export_button.setEnabled(is_plot_displayed)  # Enable button only if data is present

    def update_plugin_list(self):
        """Update the UI list with available plugins."""
        print("Updating plugin list...")
        plugins = self.controller.get_plugins()

        # Clear the current list
        self.plugins_list.clear()

        # Populate the plugin list
        for plugin_name in plugins:
            item = QListWidgetItem(plugin_name)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.plugins_list.addItem(item)

    def __del__(self):
        print(f"OsmoUI {self} deleted")
