from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QInputDialog, \
    QMessageBox, QLabel, QStackedWidget
from PySide6.QtCore import Qt

from src.controllers.view_controller import ViewController
from src.ui.measurement_ui import MeasurementUI
from src.ui.widgets.preferences_dialog import PreferencesDialog
from src.ui.widgets.settings_dialog import ViewSettingsDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.preferences_action = None
        self.empty_message_label = QLabel(
            "Create a new analysis by going to File/New Analysis.", self
        )
        self.stacked_widget = QStackedWidget(self)
        self.tabs = QTabWidget(self)
        self.ui_views = []  # List to store UI instances (views)

        self.setWindowTitle("L.A.S.T")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(600, 400)

        self.settings_action = None
        self.new_analysis_action = None

        # Set up the central widget and layout
        self.setup_central_widget()

        # Set up the menu bar
        self.setup_menu_bar()

    def setup_central_widget(self):
        """Set up central widget and its layout."""
        central_widget = QWidget(self)
        central_layout = QVBoxLayout(central_widget)

        # Create a stacked widget to switch between tabs and message
        central_layout.addWidget(self.stacked_widget)

        # Tab widget
        self.stacked_widget.addWidget(self.tabs)

        # Placeholder message when no tabs are present
        self.empty_message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stacked_widget.addWidget(self.empty_message_label)

        # Set tabs to be closable
        self.tabs.setTabsClosable(True)

        # Set central widget
        self.setCentralWidget(central_widget)

        # Connect tab close signal
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # Update the view to reflect if tabs are empty
        self.update_empty_message()

    def setup_menu_bar(self):
        """Set up the menu bar with File/New Analysis."""
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")

        # New Analysis action
        self.new_analysis_action = QAction("New Analysis", self)
        self.new_analysis_action.triggered.connect(self.create_tab)
        self.new_analysis_action.setShortcut("Ctrl+N")
        file_menu.addAction(self.new_analysis_action)

        # Settings menu
        self.settings_action = QAction("View Settings", self)
        self.settings_action.triggered.connect(self.open_view_settings)
        file_menu.addAction(self.settings_action)

        #Preferences action
        self.preferences_action = QAction("Preferences", self)
        self.preferences_action.triggered.connect(self.open_preferences)
        file_menu.addAction(self.preferences_action)

        # Initial state for the settings action
        self.settings_action.setEnabled(False)  # Disable initially

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

        # Update the view to reflect if tabs are empty after adding
        self.update_empty_message()

        # Enable the View Settings action if there is at least one tab
        self.update_settings_action_state()

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
                # Check if cleanup method exists before calling it
                if hasattr(tab_widget, 'cleanup'):
                    tab_widget.cleanup()
                self.ui_views.remove(tab_widget)

            # Remove the tab
            self.tabs.removeTab(index)

        # Update the view to reflect if tabs are empty after closing
        self.update_empty_message()

        # Update the settings action state after tab removal
        self.update_settings_action_state()

    def update_empty_message(self):
        """Update visibility of the empty message when there are no tabs."""
        if self.tabs.count() == 0:
            self.stacked_widget.setCurrentWidget(self.empty_message_label)
        else:
            self.stacked_widget.setCurrentWidget(self.tabs)

    def update_settings_action_state(self):
        """Enable the View Settings action if there's at least one tab, otherwise disable it."""
        if self.tabs.count() > 0:
            self.settings_action.setEnabled(True)
        else:
            self.settings_action.setEnabled(False)

    def open_view_settings(self):
        """Open the settings dialog for the currently active view."""
        active_tab_index = self.tabs.currentIndex()
        if active_tab_index != -1:  # Make sure there's at least one tab
            active_ui = self.tabs.widget(active_tab_index)  # Get the current tab's UI instance
            if hasattr(active_ui, 'controller'):
                settings_dialog = ViewSettingsDialog(active_ui.controller, self)
                settings_dialog.exec()

    def open_preferences(self):
        preferences_dialog = PreferencesDialog(self)
        preferences_dialog.exec()
