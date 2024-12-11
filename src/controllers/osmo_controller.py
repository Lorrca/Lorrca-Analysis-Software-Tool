import logging

from src.controllers.plugin_manager import PluginManager
from src.models.model_container import ModelContainer
from src.views.plot_manager import PlotManager

# Set up logging configuration
logger = logging.getLogger(__name__)


class OsmoController:
    def __init__(self):
        self.model_container = ModelContainer()  # Store models and sets
        self.plot_manager = PlotManager()
        self.plugin_manager = PluginManager()

    def load_files(self, file_paths, batch=False):
        """Load files and delegate storage to the container, handling batch or individual processing."""
        try:
            if batch:
                # Process as a batch
                self.model_container.load_files(file_paths, batch=True)
                logger.info(f"Batch of {len(file_paths)} files successfully processed.")
            else:
                # Process each file individually
                self.model_container.load_files(file_paths, batch=False)
                logger.info(f"{len(file_paths)} files successfully processed individually.")

            # Print all models after loading
            self.model_container.print_all_models()
            return True
        except Exception as e:
            logger.error(f"Error during loading files: {e}")
            return False

    def get_updated_canvas(self, selected_element_ids):
        """Ask PlotManager to visualize only selected elements and return the canvas."""
        self.plot_manager.visualize_selected_elements(selected_element_ids)
        logger.info("Canvas updated with selected elements.")
        return self.plot_manager.get_figure()

    def get_plugins(self):
        """Retrieve the list of discovered plugins, including their IDs."""
        if not self.plugin_manager.plugins:
            logger.info("Loading plugins...")
            self.plugin_manager.load_plugins(self.model_container, self.plot_manager)
        else:
            logger.info("Plugins already loaded.")

        plugins_info = self.plugin_manager.get_all_plugin_info()
        logger.info(f"Retrieved plugins: {plugins_info}")
        return plugins_info

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

    def remove_elements_by_plugin_id(self, plugin_id):
        self.plot_manager.remove_elements_by_plugin_id(plugin_id)

    def save_plot(self, filename, width, height, dpi, x_label, y_label, title):
        """Delegate the save plot operation to PlotManager."""
        self.plot_manager.save_plot(
            filename, width, height, dpi, x_label, y_label, title
        )

    def __del__(self):
        """Clean up when the controller is deleted."""
        logger.info(f"Controller {self} deleted.")
