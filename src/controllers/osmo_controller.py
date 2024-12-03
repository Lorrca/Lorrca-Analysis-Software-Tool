import logging
from src.controllers.plugin_manager import PluginManager
from src.views.plot_manager import PlotManager
from src.utils.osmo_data_loader import load_data

# Set up logging configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class OsmoController:
    def __init__(self):
        self.model = None
        self.plot_manager = PlotManager()
        self.plugin_manager = PluginManager()

    def load_file(self, file_path):
        """Load the file and initialize the model."""
        self.model = load_data(file_path)
        if self.model is not None:
            logger.info(f"File loaded successfully: {file_path}")
            return True
        logger.error(f"Failed to load file: {file_path}")
        return False

    def get_updated_canvas(self, selected_element_ids):
        """Ask PlotManager to visualize only selected elements and return the canvas."""
        self.plot_manager.visualize_selected_elements(selected_element_ids)
        logger.info("Canvas updated with selected elements.")
        return self.plot_manager.get_figure()

    def get_plugins(self):
        """Retrieve the list of discovered plugins, including their IDs."""
        if self.model is None:
            logger.warning("No model is loaded. Cannot retrieve plugins.")
            return []

        if not self.plugin_manager.plugins:  # Check if plugins are already loaded
            logger.info("Loading plugins...")
            self.plugin_manager.load_plugins(self.model, self.plot_manager)
        else:
            logger.info("Plugins already loaded.")

        plugins_info = self.plugin_manager.get_all_plugin_info()
        logger.info(f"Retrieved plugins: {plugins_info}")
        return plugins_info

    def get_elements_by_plugin_id(self, plugin_id):
        """Retrieve all elements created by a specific plugin."""
        if not self.plugin_manager.is_plugin_loaded(plugin_id):
            logger.warning(f"Plugin with ID {plugin_id} is not loaded.")
            return []

        elements = [element for element in
                    self.plot_manager.get_all_elements().values() if
                    element.plugin_id == plugin_id]
        logger.info(
            f"Retrieved {len(elements)} elements for plugin ID {plugin_id}.")
        return elements

    def reset_plugin(self, plugin_id):
        """Reset a specific plugin (cleanup its internal state)."""
        plugin = self.plugin_manager.get_plugin_by_id(plugin_id)
        if plugin:
            plugin.cleanup()
            logger.info(f"Plugin {plugin_id} has been reset.")
        else:
            logger.warning(f"Plugin {plugin_id} not found.")

    def run_plugin(self, plugin_ids):
        """Run the plugin(s) with the provided plugin IDs."""
        for plugin_id in plugin_ids:
            self.plugin_manager.run_plugin(plugin_id)
            logger.info(
                f"Ran plugin {plugin_id}. Elements after running: {self.plot_manager.get_all_elements()}")

    def get_all_elements(self):
        """Retrieve all elements for listing."""
        elements = self.plot_manager.get_all_elements()
        logger.info(f"Retrieved {len(elements)} elements.")
        return elements

    def set_element_selection(self, element_id, is_selected):
        """Set the selection state for a given element."""
        element = self.plot_manager.get_element_by_id(element_id)
        if element:
            element.set_selected(is_selected)
            logger.info(
                f"Element {element_id} selection state set to {is_selected}.")
        else:
            logger.warning(f"Element {element_id} not found in PlotManager.")

    def draw_elements(self):
        """Draw only selected elements."""
        self.plot_manager.visualize_selected_elements()
        logger.info("Redrew canvas with only selected elements.")

    def __del__(self):
        """Clean up when the controller is deleted."""
        logger.info(f"Controller {self} deleted.")
