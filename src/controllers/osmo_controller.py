from src.controllers.plugin_manager import PluginManager
from src.views.plot_manager import PlotManager

from src.utils.osmo_data_loader import load_data

class OsmoController:
    def __init__(self):
        self.model = None
        self.data_loaded = False
        self.plugin_manager = None
        self.plot_manager = None

    def load_file(self, file_path):
        """Load the file and initialize model, plot manager, and plugin manager."""
        self.model = load_data(file_path)
        if self.model is not None:
            # Initialize plot manager and plugin manager after model is loaded
            self.plot_manager = PlotManager()
            self.plugin_manager = PluginManager(self.model, self.plot_manager)
            return True
        return False

    def get_figure(self):
        """Retrieve the figure from plot manager."""
        return self.plot_manager.get_figure() if self.plot_manager else None

    def get_plugins(self):
        """Retrieve the list of discovered plugins, including their IDs."""
        if self.plugin_manager:
            self.plugin_manager.load_plugins()
            return self.plugin_manager.get_all_plugin_info()
        return []

    def run_plugin(self, plugin_ids):
        """Run the plugin(s) with the provided plugin IDs."""
        print("running plugin")
        if self.plugin_manager:
            self.plugin_manager.run_plugin(plugin_ids)

    def get_elements(self):
        """Retrieve all elements for plotting."""
        if self.plot_manager:
            return self.plot_manager.get_all_elements()
        return []

    def draw_elements(self, element_ids):
        """Draw selected elements."""
        if self.plot_manager:
            self.plot_manager.visualize_selected_elements(element_ids)

    def __del__(self):
        print(f"Controller {self} deleted.")
