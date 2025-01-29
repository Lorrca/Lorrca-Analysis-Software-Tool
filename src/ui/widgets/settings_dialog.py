from functools import partial

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
    QStackedWidget, QFrame, QSizePolicy, QSpacerItem, QListWidgetItem, QLabel, QWidget
)
from PySide6.QtCore import Qt


class ViewSettingsDialog(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("View Settings")

        # Main layout
        self.layout = QHBoxLayout(self)

        # Sidebar with buttons
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.setSpacing(0)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)

        self.plugins_button = QPushButton("Plugins")
        self.plugins_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.plugins_button.clicked.connect(self.show_plugins)
        self.sidebar_layout.addWidget(self.plugins_button)

        self.hc_button = QPushButton("Healthy Control")
        self.hc_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.hc_button.clicked.connect(self.show_healthy_control)
        self.sidebar_layout.addWidget(self.hc_button)

        # Adding vertical space under buttons
        self.vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                           QSizePolicy.Policy.Expanding)
        self.sidebar_layout.addItem(self.vertical_spacer)

        self.layout.addLayout(self.sidebar_layout)

        # Divider line between sidebar and content area
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.layout.addWidget(self.line)

        # Main content area (stacked widget to switch between plugins and HC)
        self.main_content = QStackedWidget(self)
        self.layout.addWidget(self.main_content)

        # Plugin list (will be shown in main content area when Plugins is selected)
        self.plugin_list = QListWidget(self)
        self.main_content.addWidget(self.plugin_list)

        # Healthy Control section
        self.hc_widget = QWidget()
        self.hc_layout = QVBoxLayout(self.hc_widget)

        # HC Plugins list
        self.hc_plugins_label = QLabel("HC Plugins", self.hc_widget)
        self.hc_layout.addWidget(self.hc_plugins_label)

        self.hc_plugins_list = QListWidget(self.hc_widget)
        self.hc_layout.addWidget(self.hc_plugins_list)

        # HC Models list
        self.hc_models_label = QLabel("HC Models", self.hc_widget)
        self.hc_layout.addWidget(self.hc_models_label)

        self.hc_models_list = QListWidget(self.hc_widget)
        self.hc_layout.addWidget(self.hc_models_list)

        # "Update Canvas" button
        self.update_canvas_button = QPushButton("Update Canvas", self.hc_widget)
        self.update_canvas_button.clicked.connect(self.update_canvas)
        self.hc_layout.addWidget(self.update_canvas_button)

        # Add HC section to the main content area
        self.main_content.addWidget(self.hc_widget)

        # Set the minimum size of the window
        self.setMinimumSize(400, 300)

        # Update the plugin list on initialization
        self.update_plugin_list()

    def show_plugins(self):
        """Show the Plugins list in the main content area."""
        self.update_plugin_list()
        self.main_content.setCurrentWidget(self.plugin_list)

    def show_healthy_control(self):
        """Show the Healthy Control section in the main content area."""
        self.update_healthy_control_lists()
        self.main_content.setCurrentWidget(self.hc_widget)

    def update_plugin_list(self):
        """Update the plugin list with checkboxes."""
        self.plugin_list.clear()
        plugins = self.controller.get_plugins()

        for plugin in plugins:
            item = QListWidgetItem(plugin["name"])
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)

            # Set the initial check state based on the plugin's selection
            item.setCheckState(
                Qt.CheckState.Checked if plugin["selected"] else Qt.CheckState.Unchecked)
            item.setData(Qt.ItemDataRole.UserRole, plugin["id"])  # Store plugin_id in the item data
            self.plugin_list.addItem(item)

        self.plugin_list.itemChanged.connect(self.handle_plugin_item_changed)

    def update_healthy_control_lists(self):
        """Update the HC Plugins and Models lists with checkboxes."""
        self.hc_plugins_list.clear()
        self.hc_models_list.clear()

        # Update HC Plugins
        hc_plugins = self.controller.get_hc_plugins()
        for plugin in hc_plugins:
            item = QListWidgetItem(plugin["name"])
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(
                Qt.CheckState.Checked if plugin["selected"] else Qt.CheckState.Unchecked)
            item.setData(Qt.ItemDataRole.UserRole, plugin["id"])
            self.hc_plugins_list.addItem(item)

        # Update HC Models
        hc_models = self.controller.get_hc_models()
        for model, selected in hc_models:
            item = QListWidgetItem(model.name)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked if selected else Qt.CheckState.Unchecked)
            item.setData(Qt.ItemDataRole.UserRole, model.id)
            self.hc_models_list.addItem(item)

        self.hc_plugins_list.itemChanged.connect(
            partial(self.handle_plugin_item_changed, is_hc=True))
        self.hc_models_list.itemChanged.connect(self.handle_model_item_changed)

    def handle_model_item_changed(self, item):
        model_id = item.data(Qt.ItemDataRole.UserRole)
        selected = item.checkState() == Qt.CheckState.Checked
        self.controller.update_model_selection(model_id, selected)

    def handle_plugin_item_changed(self, item, is_hc=False):
        """Handle state change of the plugin list item."""
        plugin_id = item.data(Qt.ItemDataRole.UserRole)
        selected = item.checkState() == Qt.CheckState.Checked
        self.controller.update_plugin_selection(plugin_id, selected, is_hc)

    def update_canvas(self):
        """Handle the Update Canvas button click."""
        # Logic to update the canvas goes here
        self.controller.update_canvas()
