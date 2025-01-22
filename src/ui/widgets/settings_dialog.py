from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, \
    QStackedWidget, QFrame, QSizePolicy, QSpacerItem, QListWidgetItem
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

        # Healthy Control list (will be shown in main content area when HC is selected)
        self.hc_list = QListWidget(self)
        self.main_content.addWidget(self.hc_list)

        # Set the minimum size of the window
        self.setMinimumSize(400, 300)

        # Update the plugin list on initialization
        self.update_plugin_list()
        self.update_healthy_control_list()

    def show_plugins(self):
        """Show the Plugins list in the main content area."""
        self.main_content.setCurrentWidget(self.plugin_list)

    def show_healthy_control(self):
        """Show the Healthy Control list in the main content area."""
        self.main_content.setCurrentWidget(self.hc_list)

    def update_plugin_list(self):
        """Update the plugin list with checkboxes."""
        self.plugin_list.clear()
        plugins = self.controller.plugin_manager.get_plugins()

        for plugin in plugins:
            item = QListWidgetItem(plugin["name"])
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)

            # Set the initial check state based on the plugin's selection
            if plugin["selected"]:
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)

            # Connect the item state change (itemChanged signal) to the controller's method
            item.setData(Qt.ItemDataRole.UserRole, plugin["id"])  # Store plugin_id in the item data
            self.plugin_list.addItem(item)

        # Connect the itemChanged signal for all items to handle state change
        self.plugin_list.itemChanged.connect(self.handle_item_changed)

    def update_healthy_control_list(self):
        """Update the plugin list with checkboxes."""
        self.hc_list.clear()
        hc_plugins = self.controller.plugin_manager.get_hc_plugins()

        for plugin in hc_plugins:
            item = QListWidgetItem(plugin["name"])
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)

            # Set the initial check state based on the plugin's selection
            if plugin["selected"]:
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)

            # Connect the item state change (itemChanged signal) to the controller's method
            item.setData(Qt.ItemDataRole.UserRole, plugin["id"])  # Store plugin_id in the item data
            self.hc_list.addItem(item)

        # Connect the itemChanged signal for all items to handle state change
        self.hc_list.itemChanged.connect(self.handle_item_changed)

    def handle_item_changed(self, item):
        """Handle state change of the list item."""
        plugin_id = item.data(Qt.ItemDataRole.UserRole)  # Retrieve the plugin ID
        selected = item.checkState() == Qt.CheckState.Checked
        self.controller.update_plugin_selection(plugin_id, selected)
