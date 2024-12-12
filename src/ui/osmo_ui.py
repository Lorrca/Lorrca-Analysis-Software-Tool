import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QLabel, QListWidget, QPushButton, \
    QWidget, QStackedLayout, QListWidgetItem, QSizePolicy, QDialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from src.ui.widgets.drag_drop_widget import DragDropWidget
from src.ui.widgets.export_dialog import ExportDialog

logger = logging.getLogger(__name__)


class OsmoUI(QWidget):
    def __init__(self, osmo_controller):
        super().__init__()
        self.controller = osmo_controller

        self.main_frame = QFrame(self)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(self.main_frame)
        self.setLayout(self.main_layout)

        self.drag_drop_widget = DragDropWidget(self.load_files)
        self.main_frame_layout = QStackedLayout(self.main_frame)
        self.main_frame_layout.addWidget(self.drag_drop_widget)

        self.left_layout = None
        self.right_layout = None
        self.figure = None
        self.canvas = None
        self.plugins_list = None
        self.elements_list = None
        self.export_button = None

    def setup_main_layout(self):
        horizontal_layout = QHBoxLayout()

        left_frame = QFrame(self.main_frame)
        self.left_layout = QVBoxLayout(left_frame)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.left_layout.addWidget(self.canvas)

        self.export_button = QPushButton("Export", self)
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(self.open_export_dialog)
        self.left_layout.addWidget(self.export_button)
        horizontal_layout.addWidget(left_frame, stretch=1)

        right_frame = QFrame(self.main_frame)
        self.right_layout = QVBoxLayout(right_frame)

        plugins_label = QLabel("Plugins", self)
        self.right_layout.addWidget(plugins_label)

        self.plugins_list = QListWidget(self)
        self.plugins_list.itemChanged.connect(self.on_plugin_selection_changed)
        self.right_layout.addWidget(self.plugins_list)

        refresh_button = QPushButton("Refresh Plugins", self)
        refresh_button.clicked.connect(self.update_plugin_list)
        self.right_layout.addWidget(refresh_button)

        elements_label = QLabel("Elements", self)
        self.right_layout.addWidget(elements_label)

        self.elements_list = QListWidget(self)
        self.elements_list.itemChanged.connect(self.on_element_selection_changed)
        self.right_layout.addWidget(self.elements_list)

        horizontal_layout.addWidget(right_frame)
        main_widget = QWidget()
        main_widget.setLayout(horizontal_layout)
        self.main_frame_layout.addWidget(main_widget)
        self.main_frame_layout.setCurrentWidget(main_widget)

    def load_files(self, file_paths):
        if self.controller.load_files(file_paths):
            self.setup_main_layout()
            self.update_plugin_list()
            self.update_elements_list()
        else:
            logger.error("Error loading files.")

    def update_canvas(self):
        if self.figure:
            selected_element_ids = [
                self.elements_list.item(index).data(Qt.ItemDataRole.UserRole)
                for index in range(self.elements_list.count())
                if self.elements_list.item(index).checkState() == Qt.CheckState.Checked
            ]
            self.figure = self.controller.get_updated_canvas(selected_element_ids)
            self.canvas.figure = self.figure
            self.canvas.draw()
            self.export_button.setEnabled(any(ax.has_data() for ax in self.figure.axes))

    def update_plugin_list(self):
        plugins = self.controller.get_plugins()
        self.plugins_list.clear()

        for plugin in plugins:
            item = QListWidgetItem(plugin["name"])
            item.setData(Qt.ItemDataRole.UserRole, plugin["id"])
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.plugins_list.addItem(item)

    def update_elements_list(self):
        self.elements_list.clear()
        elements = self.controller.get_all_elements()
        for element_id, element in elements.items():
            item = QListWidgetItem(f"{element.label}, {element.plugin_name}")
            item.setData(Qt.ItemDataRole.UserRole, element_id)
            item.setCheckState(
                Qt.CheckState.Checked if element.selected else Qt.CheckState.Unchecked)
            self.elements_list.addItem(item)

    def on_plugin_selection_changed(self, item):
        plugin_id = item.data(Qt.ItemDataRole.UserRole)
        if item.checkState() == Qt.CheckState.Checked:
            self.controller.run_plugin([plugin_id])
            self.update_elements_list()
            self.update_canvas()
        else:
            self.controller.remove_elements_by_plugin_id(plugin_id)
            self.update_elements_list()
            self.update_canvas()

    def on_element_selection_changed(self):
        self.update_canvas()

    def open_export_dialog(self):
        dialog = ExportDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            settings = dialog.get_settings()
            if settings:
                if self.controller.export_image(
                        settings["filename"], self.figure, settings["width"],
                        settings["height"], settings["dpi"], settings["x_label"],
                        settings["y_label"], settings["title"]):
                    logger.info(f"Image successfully saved to {settings['filename']}")
                else:
                    logger.error("Export failed.")

    def cleanup(self):
        """Detach controller from the view."""
        self.controller = None
