import os
from PySide6.QtCore import Qt, QModelIndex, QDir, QUrl
from PySide6.QtGui import QColor, QPainter, QAction, QDesktopServices
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QTreeView, QSizePolicy, \
    QFileSystemModel, QMenu, QStyledItemDelegate, QWidget, QDialog, QSpacerItem, \
    QStackedWidget, QFrame, QHBoxLayout

DISABLED_SUFFIX = ".disabled"
ENABLED_SUFFIX = ".py"

current_script_dir = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(current_script_dir, "../../.."))


class DisabledItemDelegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option, index: QModelIndex):
        """Override to gray out disabled files."""
        model = index.model()
        if isinstance(model, QFileSystemModel):
            file_path = model.filePath(index)
            if file_path.endswith(DISABLED_SUFFIX):
                option.palette.setColor(option.palette.ColorRole.Text, QColor(169, 169, 169))
        super().paint(painter, option, index)


class BaseFileBrowser(QWidget):
    """Base class for file browsers to avoid code duplication."""

    def __init__(self, folder_path, name_filters=None, show_context_menu=False, parent=None):
        super().__init__(parent)

        self.folder_path = folder_path
        self.layout = QVBoxLayout(self)

        # Ensure the folder exists
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)

        # File system model setup
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(folder_path)
        self.file_model.setFilter(QDir.Filter.Files | QDir.Filter.Dirs | QDir.Filter.NoDotAndDotDot)

        if name_filters:
            self.file_model.setNameFilters(name_filters)
            self.file_model.setNameFilterDisables(False)

        # File browser setup
        self.file_browser = QTreeView(self)
        self.file_browser.setModel(self.file_model)
        self.file_browser.setRootIndex(self.file_model.index(folder_path, 0, QModelIndex()))
        self.file_browser.setColumnWidth(0, 250)
        self.file_browser.setColumnWidth(1, 100)

        # Enable context menu if required
        if show_context_menu:
            self.file_browser.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.file_browser.customContextMenuRequested.connect(self.show_context_menu)

        # Apply custom item delegate for disabled files
        self.file_browser.setItemDelegate(DisabledItemDelegate(self))

        self.layout.addWidget(self.file_browser)

        # Button to open folder in file explorer
        self.open_explorer_button = QPushButton(f"Open {self.windowTitle()} Folder")
        self.open_explorer_button.setSizePolicy(QSizePolicy.Policy.Minimum,
                                                QSizePolicy.Policy.Fixed)
        self.open_explorer_button.clicked.connect(lambda: open_folder(folder_path))
        self.layout.addWidget(self.open_explorer_button)

    def show_context_menu(self, position):
        """To be implemented in subclasses if needed."""
        pass


class PluginView(BaseFileBrowser):
    def __init__(self, folder_path, parent=None):
        super().__init__(folder_path, name_filters=["*.py", "*.py.disabled"],
                         show_context_menu=True, parent=parent)

    def show_context_menu(self, position):
        """Show context menu for enabling/disabling plugins."""
        index = self.file_browser.indexAt(position)
        if not index.isValid():
            return

        file_path = self.file_model.filePath(index)
        file_name = os.path.basename(file_path)

        menu = QMenu(self)

        if file_name.endswith(DISABLED_SUFFIX):
            enable_action = QAction("Enable", self)
            enable_action.triggered.connect(lambda: self.toggle_plugin(file_path, enable=True))
            menu.addAction(enable_action)
        elif file_name.endswith(ENABLED_SUFFIX):
            disable_action = QAction("Disable", self)
            disable_action.triggered.connect(lambda: self.toggle_plugin(file_path, enable=False))
            menu.addAction(disable_action)

        menu.exec(self.file_browser.viewport().mapToGlobal(position))

    def toggle_plugin(self, file_path, enable):
        """Toggle plugin between enabled and disabled states."""
        dir_path, file_name = os.path.split(file_path)

        if enable:
            new_name = file_name.replace(ENABLED_SUFFIX + DISABLED_SUFFIX, ENABLED_SUFFIX)
        else:
            new_name = file_name + DISABLED_SUFFIX

        new_path = os.path.join(dir_path, new_name)
        os.rename(file_path, new_path)

        # Refresh the file model to reflect changes
        self.file_model.setRootPath(self.file_model.rootPath())

        # Optionally update file styles
        self.file_browser.viewport().update()


class HealthyControlView(BaseFileBrowser):
    def __init__(self, folder_path, parent=None):
        super().__init__(folder_path, name_filters=["*.csv"], show_context_menu=False,
                         parent=parent)


class PreferencesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.plugins_root = os.path.join(PROJECT_ROOT, "plugins")
        self.healthy_control_root = os.path.join(PROJECT_ROOT, "HC")

        self.setWindowTitle("Preferences")

        self.layout = QHBoxLayout(self)
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.setSpacing(0)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)

        # Plugins button
        self.plugins_button = QPushButton("Plugins")
        self.plugins_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.plugins_button.clicked.connect(self.show_plugins)
        self.sidebar_layout.addWidget(self.plugins_button)

        # Healthy Control button
        self.healthy_control_button = QPushButton("Healthy Control")
        self.healthy_control_button.setSizePolicy(QSizePolicy.Policy.Minimum,
                                                  QSizePolicy.Policy.Fixed)
        self.healthy_control_button.clicked.connect(self.show_healthy_control)
        self.sidebar_layout.addWidget(self.healthy_control_button)

        self.vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                           QSizePolicy.Policy.Expanding)
        self.sidebar_layout.addItem(self.vertical_spacer)

        self.layout.addLayout(self.sidebar_layout)

        # Divider line
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.layout.addWidget(self.line)

        # Stacked widget for content area
        self.main_content = QStackedWidget(self)
        self.layout.addWidget(self.main_content)

        # Plugins container setup
        self.plugins_container = PluginView(self.plugins_root)
        self.main_content.addWidget(self.plugins_container)

        # Healthy Control container setup
        self.healthy_control_container = HealthyControlView(self.healthy_control_root)
        self.main_content.addWidget(self.healthy_control_container)

        self.setMinimumSize(600, 400)

    def show_plugins(self):
        """Show the plugins container in the main content area."""
        self.main_content.setCurrentWidget(self.plugins_container)

    def show_healthy_control(self):
        """Show the Healthy Control container in the main content area."""
        self.main_content.setCurrentWidget(self.healthy_control_container)


def open_folder(folder):
    """Open folder in the file explorer."""
    QDesktopServices.openUrl(QUrl.fromLocalFile(folder))
