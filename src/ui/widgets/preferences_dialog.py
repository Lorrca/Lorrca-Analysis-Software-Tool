import os

from PySide6.QtCore import Qt, QModelIndex, QDir
from PySide6.QtGui import QColor, QPainter, QAction
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QTreeView, \
    QStackedWidget, QFrame, QSizePolicy, QSpacerItem, QFileSystemModel, QMenu, QStyledItemDelegate

DISABLED_SUFFIX = ".disabled"
ENABLED_SUFFIX = ".py"


class DisabledItemDelegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option, index: QModelIndex):
        # Get the file path
        model = index.model()
        if isinstance(model, QFileSystemModel):
            file_path = model.filePath(index)

            # If the file is disabled, gray it out
            if file_path.endswith(DISABLED_SUFFIX):
                option.palette.setColor(option.palette.ColorRole.Text, QColor(169, 169, 169))

        # Call the base class paint method
        super().paint(painter, option, index)


class CustomFileSystemModel(QFileSystemModel):
    def rowCount(self, parent):
        """Override rowCount to exclude __init__.py"""
        count = super().rowCount(parent)

        if parent.isValid():
            dir_path = self.filePath(parent)
            files = [file for file in os.listdir(dir_path) if file != "__init__.py"]
            return len(files)

        return count

    def index(self, row, column, parent):
        """Override index to exclude __init__.py"""
        index = super().index(row, column, parent)

        if not index.isValid():
            return index

        file_info = self.fileInfo(index)
        if file_info.fileName() == "__init__.py":
            return QModelIndex()

        return index


class PreferencesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
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

        # File system model and view setup
        self.file_model = CustomFileSystemModel()
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_script_dir, "../../.."))
        default_directory = os.path.join(project_root, "plugins")

        self.file_model.setRootPath(default_directory)
        self.file_model.setNameFilters(["*.py", "*.py.disabled"])
        self.file_model.setNameFilterDisables(False)
        self.file_model.setFilter(QDir.Filter.Files | QDir.Filter.NoDotAndDotDot)

        self.file_browser = QTreeView(self)
        self.file_browser.setModel(self.file_model)
        self.file_browser.setRootIndex(self.file_model.index(default_directory, 0, QModelIndex()))
        self.file_browser.setColumnWidth(0, 250)
        self.file_browser.setColumnWidth(1, 100)
        self.file_browser.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.file_browser.customContextMenuRequested.connect(self.show_context_menu)

        # Apply custom item delegate for disabled files
        self.file_browser.setItemDelegate(DisabledItemDelegate(self))

        self.setMinimumSize(600, 400)
        self.main_content.addWidget(self.file_browser)

    def show_plugins(self):
        """Show the file browser in the main content area."""
        self.main_content.setCurrentWidget(self.file_browser)

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
        self.update_file_styles()

    def update_file_styles(self):
        """Update styles for disabled files."""
        self.file_browser.viewport().update()
