from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFrame, QLabel,
    QListWidget, QListWidgetItem, QHBoxLayout
)
from PySide6.QtCore import Qt


class OsmoUI(QWidget):
    def __init__(self, osmo_controller):
        super().__init__()

        print(f"OsmoUI {self} created")
        self.elements_list = None
        self.elements_label = None
        self.refresh_plugins_button = None
        self.plugins_list = None
        self.plugins_label = None
        self.export_button = None
        self.data_frame = None

        self.controller = osmo_controller

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

        # Export Button
        self.export_button = QPushButton("Export", self)
        main_layout.addWidget(self.export_button)

        # Right Layout (Plugins and Elements)
        right_layout = QVBoxLayout()

        # Plugin List Section
        self.setup_plugin_list_section(right_layout)

        # Elements List Section
        self.setup_elements_list_section(right_layout)

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

    def update_plugin_list(self):
        """Update the UI list with available plugins."""
        print("Updating plugin list...")
        plugins = self.controller.get_plugins()  # Ask the controller for plugins

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
