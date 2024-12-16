from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, \
    QTabWidget, QInputDialog, QMessageBox

from src.controllers.view_controller import ViewController
from src.ui.measurement_ui import MeasurementUI


class MainWindow(QMainWindow):
    def __init__(self, main_controller):
        super().__init__()

        self.tabs = None
        self.create_view_button = None

        self.controller = main_controller
        self.ui_views = []  # List to store UI instances (views)

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
        self.create_view_button = QPushButton("Create New View", self)

        # Add buttons to the central layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_view_button)
        central_layout.addLayout(button_layout)

        # Tab widget
        self.tabs = QTabWidget(self)
        central_layout.addWidget(self.tabs)

        # Set tabs to be closable
        self.tabs.setTabsClosable(True)

        self.setCentralWidget(central_widget)

        # Connect buttons
        self.create_view_button.clicked.connect(self.create_tab)
        self.tabs.tabCloseRequested.connect(self.close_tab)

    def create_tab(self):
        """Create a new tab."""
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Tab Name")
        dialog.setLabelText("Enter a name for the tab:")
        dialog.setTextValue("New Measurement")  # Set placeholder text
        dialog.setOkButtonText("Create")
        dialog.setCancelButtonText("Cancel")

        if dialog.exec():
            name = dialog.textValue() or "New Measurement"

            ui_instance = MeasurementUI(ViewController())

            tab_index = self.tabs.addTab(ui_instance, name)
            self.tabs.setTabToolTip(tab_index, name)

            self.ui_views.append(ui_instance)

    def close_tab(self, index):
        """Close the tab at the given index with a confirmation dialog."""
        tab_widget = self.tabs.widget(index)

        # Prompt for confirmation
        reply = QMessageBox.question(
            self,
            "Close Tab Confirmation",
            "Closing this tab will discard any unsaved results. Are you sure you want to proceed?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Ensure cleanup of associated UI resources
            if tab_widget in self.ui_views:
                tab_widget.cleanup()
                self.ui_views.remove(tab_widget)

            self.tabs.removeTab(index)
