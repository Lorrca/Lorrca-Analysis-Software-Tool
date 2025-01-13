from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, \
    QStackedWidget, QFrame, QSizePolicy, QSpacerItem


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

    def show_plugins(self):
        """Show the Plugins list in the main content area."""
        self.main_content.setCurrentWidget(self.plugin_list)

    def show_healthy_control(self):
        """Show the Healthy Control list in the main content area."""
        self.main_content.setCurrentWidget(self.hc_list)
