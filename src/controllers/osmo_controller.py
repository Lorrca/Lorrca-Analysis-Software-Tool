from src.controllers.plugin_manager import PluginManager
from src.views.plot_manager import PlotManager
import os

PLUGINS_FOLDER: str = '../plugins'


class OsmoController:
    def __init__(self):
        self.data_loader = None
        self.model = None
        self.data_loaded = False
        self.plot_manager = PlotManager()

        # Dynamically determine plugin folder location relative to the application
        plugin_folder = os.path.join(os.getcwd(), PLUGINS_FOLDER)
        self.plugin_manager = PluginManager(self.model, self.plot_manager, plugin_folder)

    def get_figure(self):
        return self.plot_manager.get_figure()

    def get_plugins(self):
        return self.plugin_manager.discovered_plugins

    def draw_elements(self, elements_ids):
        self.plot_manager.visualize_selected_elements(elements_ids)

    def __del__(self):
        print(f"Controller {self} deleted.")
