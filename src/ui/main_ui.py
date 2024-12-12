from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, \
    QTabWidget, QInputDialog, QMessageBox

from src.controllers.osmo_controller import OsmoController
from src.ui.osmo_ui import OsmoUI


class MainWindow(QMainWindow):
    def __init__(self, main_controller):
        super().__init__()

        self.tabs = None
        self.create_oxy_button = None
        self.create_osmo_button = None

        self.controller = main_controller
        self.ui_views = []  # List to store OsmoUI instances (views)

        self.setWindowTitle("L.A.S.T")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(600, 400)

        # Set up the central widget and layout
        self.setup_central_widget()

    def setup_central_widget(self):
        """Set up central widget and its layout."""
        central_widget = QWidget(self)
        central_layout = QVBoxLayout(central_widget)

        # Buttons to create a new Osmo or Oxy Scan
        self.create_osmo_button = QPushButton("Create New Osmo", self)
        self.create_oxy_button = QPushButton("Create New Oxy Scan", self)

        # Add buttons to the central layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_osmo_button)
        button_layout.addWidget(self.create_oxy_button)
        central_layout.addLayout(button_layout)

        # Tab widget
        self.tabs = QTabWidget(self)
        central_layout.addWidget(self.tabs)

        # Set tabs to be closable
        self.tabs.setTabsClosable(True)

        self.setCentralWidget(central_widget)

        # Connect buttons
        self.create_osmo_button.clicked.connect(self.create_osmo_tab)
        self.tabs.tabCloseRequested.connect(self.close_tab)

    def create_osmo_tab(self):
        """Create a new tab with an OsmoUI."""
        name, ok = QInputDialog.getText(self, "Tab Name", "Enter a name for the Osmo tab:")
        if not name and ok:
            name = "Osmo"

        osmo_ui = OsmoUI(OsmoController())

        osmo_tab_index = self.tabs.addTab(osmo_ui, name)
        self.tabs.setTabToolTip(osmo_tab_index, name)

        self.ui_views.append(osmo_ui)

    def close_tab(self, index):
        """Close the tab at the given index with a confirmation dialog."""
        tab_widget = self.tabs.widget(index)

        # Check if the tab has unsaved changes and prompt for confirmation
        reply = QMessageBox.question(self, "Confirm action",
                                     "Are you sure you want to close this tab? Unsaved work will be deleted.",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            for osmo_ui in self.ui_views:
                if osmo_ui == tab_widget:
                    osmo_ui.cleanup()
                    self.tabs.removeTab(index)
                    break
