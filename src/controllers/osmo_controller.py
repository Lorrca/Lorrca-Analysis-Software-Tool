from src.controllers.plugin_manager import PluginManager
from src.views.plot_manager import PlotManager
import os

PLUGINS_FOLDER: str = '../plugins'

from src.utils.osmo_data_loader import load_data


class OsmoController:
    def __init__(self):
        self.model = None
        self.data_loaded = False
        self.plot_manager = PlotManager()

        # Dynamically determine plugin folder location relative to the application
        plugin_folder = os.path.join(os.getcwd(), PLUGINS_FOLDER)
        self.plugin_manager = PluginManager(self.model, self.plot_manager, plugin_folder)

    def load_file(self, file_path):
        self.model = load_data(file_path)
        if self.model is not None:
            return True

    def get_figure(self):
        return self.plot_manager.get_figure()

    def get_plugins(self):
        self.plugin_manager.scan_plugins()
        plugins = self.plugin_manager.discovered_plugins
        return plugins

    def draw_elements(self, elements_ids):
        self.plot_manager.visualize_selected_elements(elements_ids)

    def __del__(self):
        print(f"Controller {self} deleted.")
