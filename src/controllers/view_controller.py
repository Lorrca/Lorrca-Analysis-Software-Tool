import logging

from src.controllers.plugin_manager import PluginManager
from src.models.model_container import ModelContainer
from src.views.plot_manager import PlotManager

# Set up logging configuration
logger = logging.getLogger(__name__)


class ViewController:
    def __init__(self):
        self.view = None
        self._model_container = ModelContainer()  # Store models and sets
        self._plot_manager = PlotManager()
        self._plugin_manager = PluginManager(self._model_container)

    def register_view(self, view):
        """Register a view instance."""
        self.view = view

    def initial_file_load(self, file_paths):
        try:
            self._model_container.load_files(file_paths)
            self._plugin_manager.load_plugins(self._plot_manager)
            return True
        except Exception as e:
            logger.error(f"Error during loading files: {e}")
            return False

    def load_files(self, file_paths):
        """Load files and delegate storage to the container, handling batch or individual processing."""
        try:
            # Process each file individually
            self._model_container.load_files(file_paths)

            return True
        except Exception as e:
            logger.error(f"Error during loading files: {e}")
            return False

    def get_updated_canvas(self, selected_element_ids):
        """Ask PlotManager to visualize only selected elements and return the canvas."""
        # Visualize the selected elements and pass labels and title
        self._plot_manager.visualize_selected_elements(selected_element_ids)

        logger.info("Canvas updated with selected elements.")

        # Return the updated figure
        return self._plot_manager.get_figure()

    def run_plugin(self, plugin_id):
        """Run the plugin(s) with the provided plugin IDs."""
        self._plugin_manager.run_plugin(plugin_id)
        logger.info(
            f"Ran plugin {plugin_id}. Elements after running: {self._plot_manager.get_all_elements()}")

    def get_all_elements(self):
        """Retrieve all elements for listing."""
        elements = self._plot_manager.get_all_elements()
        logger.info(f"Retrieved {len(elements)} elements.")
        return elements

    def get_all_measurements_with_selection(self):
        return self._model_container.get_models_with_selection()

    def get_elements_by_model_id(self, model_id):
        return self._plot_manager.get_elements_by_model_id(model_id)

    def update_model_selection(self, model_id, selected):
        self._model_container.update_selection(model_id, selected)
        if selected:
            self._plugin_manager.analyze_model(model_id)
        else:
            self._plot_manager.remove_elements_by_model_id(model_id)

    def save_plot(self, filename, width, height, dpi, x_label, y_label, title):
        """Delegate the save plot operation to PlotManager."""
        self._plot_manager.save_plot(
            filename, width, height, dpi, x_label, y_label, title
        )

    def update_plugin_selection(self, plugin_id, selected):
        self._plugin_manager.set_plugin_selection(plugin_id, selected)

        if self.view:
            self.view.update_measurement_tree_widget()
        else:
            logger.warning("View is not registered. Measurement tree update skipped.")

    def get_plugins(self):
        return self._plugin_manager.get_plugins()

    def get_hc_plugins(self):
        return self._plugin_manager.get_plugins(hc_plugins=True)

    def get_hc_models(self):
        return self._model_container.get_hc_models_with_selection()

    def __del__(self):
        """Notify when the controller is deleted."""
        logger.info(f"Controller {self} deleted.")
