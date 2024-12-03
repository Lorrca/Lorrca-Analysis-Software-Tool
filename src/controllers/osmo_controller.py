from src.controllers.plugin_manager import PluginManager
from src.views.plot_manager import PlotManager

from src.utils.osmo_data_loader import load_data


class OsmoController:
    def __init__(self):
        self.model = None
        self.plot_manager = PlotManager()
        self.plugin_manager = PluginManager()

    def load_file(self, file_path):
        """Load the file and initialize model"""
        self.model = load_data(file_path)
        if self.model is not None:
            return True
        return False

    def get_updated_canvas(self, element_ids):
        """Ask PlotManager to visualize selected elements and return the canvas."""
        self.plot_manager.visualize_selected_elements(element_ids)
        return self.plot_manager.get_figure()

    def get_plugins(self):
        """Retrieve the list of discovered plugins, including their IDs."""
        if self.model is None:
            print("No model is loaded. Cannot retrieve plugins.")
            return []

        if not self.plugin_manager.plugins:  # Check if plugins are already loaded
            print("Loading plugins...")
            self.plugin_manager.load_plugins(self.model, self.plot_manager)
        else:
            print("Plugins already loaded.")

        return self.plugin_manager.get_all_plugin_info()

    def get_elements_by_plugin_id(self, plugin_id):
        """Retrieve all elements created by a specific plugin."""
        if not self.plugin_manager.is_plugin_loaded(plugin_id):
            print(f"Plugin with ID {plugin_id} is not loaded.")
            return []

        # Find elements that belong to the given plugin ID
        return [element for element in
                self.plot_manager.get_all_elements().values() if
                element.plugin_id == plugin_id]

    def reset_plugin(self, plugin_id):
        """Reset a specific plugin (cleanup its internal state)."""
        plugin = self.plugin_manager.get_plugin_by_id(plugin_id)
        if plugin:
            plugin.cleanup()
            print(f"Plugin {plugin_id} has been reset.")
        else:
            print(f"Plugin {plugin_id} not found.")

    def run_plugin(self, plugin_ids):
        """Run the plugin(s) with the provided plugin IDs."""
        for plugin_id in plugin_ids:
            self.plugin_manager.run_plugin(plugin_id)
            print(self.plot_manager.get_all_elements())

    def get_all_elements(self):
        """Retrieve all elements for list."""
        return self.plot_manager.get_all_elements()

    def draw_elements(self, element_ids):
        """Draw selected elements."""
        self.plot_manager.visualize_selected_elements(element_ids)

    def __del__(self):
        """Clean up when the controller is deleted."""
        print(f"Controller {self} deleted.")
