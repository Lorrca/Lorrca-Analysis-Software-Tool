import importlib
import inspect
import logging
import os

from src.base_classes.base_batch_plugin import BaseBatchPlugin
from src.base_classes.base_plugin import BasePlugin
from src.base_classes.base_scan_model import BaseScanModel
from src.models.batch_model import BatchModel

PLUGINS_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                              '../plugins')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PluginManager:
    def __init__(self, model_container):
        self.model_container = model_container
        self.plugins = {}
        self.plugin_selection = {}  # Dictionary to store the selection state of plugins
        self.plot_manager = None

    def load_plugins(self, plot_manager):
        """Loads all plugins from the plugins folder."""
        self.plot_manager = plot_manager
        if not os.path.isdir(PLUGINS_FOLDER):
            logger.info(f"Plugins folder does not exist. Creating: {PLUGINS_FOLDER}")
            os.makedirs(PLUGINS_FOLDER, exist_ok=True)

        for file_name in os.listdir(PLUGINS_FOLDER):
            if file_name.endswith(".py") and file_name != "__init__.py":
                plugin_name = file_name[:-3]
                self._load_plugin(plugin_name)

    def _load_plugin(self, plugin_name):
        """Loads a single plugin by its name."""
        try:
            plugin_module = importlib.import_module(f"plugins.{plugin_name}")
            for attr_name in dir(plugin_module):
                attr = getattr(plugin_module, attr_name)
                # Ensure attr is a class, a subclass of BasePlugin, and not an abstract class
                if (
                        isinstance(attr, type)
                        and issubclass(attr, BasePlugin)
                        and attr is not BasePlugin
                        and not inspect.isabstract(attr)
                ):
                    plugin_instance = attr(self.plot_manager)

                    # Filter for plugins based on type of the measurements eg. Osmo, Oxy .etc
                    if self.model_container.model_type.value != plugin_instance.plugin_type.value:
                        logger.info(
                            f"Skipping plugin {plugin_instance.plugin_name} "
                            f"due to type mismatch: {plugin_instance.plugin_type} "
                            f"{self.model_container.model_type}"
                        )
                        return

                    if plugin_instance.id in self.plugins:
                        logger.warning(f"Duplicate plugin ID {plugin_instance.id}. Skipping...")
                        return

                    # Store plugin instance
                    self.plugins[plugin_instance.id] = plugin_instance
                    # Set default selection state to True
                    if isinstance(plugin_instance, BaseBatchPlugin):
                        self.plugin_selection[plugin_instance.id] = False
                    else:
                        self.plugin_selection[plugin_instance.id] = True
                    logger.info(f"Loaded plugin {plugin_instance.plugin_name}")
                    return
        except Exception as e:
            logger.error(f"Error loading plugin {plugin_name}: {e}")

    def run_plugin(self, plugin_id):
        """Run the plugin_instance for each selected model."""
        plugin_instance = self.plugins.get(plugin_id)
        if not plugin_instance:
            logger.warning(f"Plugin with ID {plugin_id} not found.")
            return

        try:
            if isinstance(plugin_instance, BaseBatchPlugin):
                self._run_batch_plugin(plugin_instance)
            elif isinstance(plugin_instance, BasePlugin):
                self._run_base_plugin(plugin_instance)
        except Exception as e:
            logger.error(f"Error running plugin_instance {plugin_instance.plugin_name}: {e}")

    def _run_batch_plugin(self, plugin_instance):
        """Run the Batch plugin for all Batch models."""
        selected_models = self.model_container.get_selected_batch_models()
        if not selected_models:
            logger.warning("No models selected to run the plugin on.")
            return

        for batch_model in selected_models:
            plugin_instance.run_plugin(batch_model)

        logger.info(f"Ran plugin: {plugin_instance.plugin_name} on selected models.")

    def _run_base_plugin(self, plugin_instance):
        """Run the base plugin for selected models."""
        selected_models = self.model_container.get_selected_models()
        if not selected_models:
            logger.warning("No models selected to run the plugin on.")
            return

        for model in selected_models:
            plugin_instance.run_plugin(model)

        logger.info(f"Ran plugin: {plugin_instance.plugin_name} on selected models.")

    def analyze_model(self, model_id: str):
        """
        Analyzes the specified model by running all available selected plugins on it.

        Args:
        model_id (str): The unique identifier of the model to be analyzed.
        """
        try:
            # Retrieve the model using its ID
            model = self.model_container.get_model_by_id(model_id)
            if not model:
                logger.warning(f"Model with ID {model_id} not found.")
                return

            # Determine the plugin type based on the model type
            plugin_class = None
            if isinstance(model, BatchModel):
                plugin_class = BaseBatchPlugin
            elif isinstance(model, BaseScanModel):
                plugin_class = BasePlugin

            if plugin_class is None:
                logger.warning(f"Unsupported model type for model ID {model_id}.")
                return

            # Iterate through the plugins and run the selected ones that match the plugin class
            for plugin_id, plugin in self.plugins.items():
                if self.plugin_selection.get(plugin_id, False):  # Check if the plugin is selected
                    if isinstance(plugin, plugin_class):
                        logger.info(f"Running plugin: {plugin.plugin_name} on model ID {model_id}")
                        try:
                            plugin.run_plugin(model)  # Run the plugin on the model
                            logger.info(f"Ran plugin: {plugin.plugin_name} successfully.")
                        except Exception as e:
                            logger.error(
                                f"Error running plugin {plugin.plugin_name} on model {model_id}: {e}")
        except Exception as e:
            logger.error(f"Error analyzing model {model_id}: {e}")

    def get_all_plugin_info(self):
        """Return a list of dictionaries containing plugin IDs, names, and selection state."""
        return [{"id": plugin.id, "name": plugin.plugin_name,
                 "selected": self.plugin_selection.get(plugin.id, False)}
                for plugin in self.plugins.values()]

    def get_plugin_by_id(self, plugin_id):
        """Return the plugin object by its ID."""
        return self.plugins.get(plugin_id)

    def set_plugin_selection(self, plugin_id, selected):
        """Set the selection state for a plugin."""
        if plugin_id in self.plugins:
            self.plugin_selection[plugin_id] = selected
            logger.info(f"Plugin {self.plugins[plugin_id].plugin_name} selection set to {selected}")
            if selected:
                self.run_plugin(plugin_id)
            else:
                self.plot_manager.remove_elements_by_plugin_id(plugin_id)
        else:
            logger.warning(f"Plugin with ID {plugin_id} not found.")

    def get_plugins(self, batch_plugins=False):
        """
        Return a list of plugins with their selection state.

        :param batch_plugins: If True, return only Batch plugins (BaseBatchPlugin).
                           If False, return only standard plugins (BasePlugin excluding BaseBatchPlugin).
        """

        def is_valid_plugin(plugin):
            return (
                isinstance(plugin, BaseBatchPlugin) if batch_plugins
                else isinstance(plugin, BasePlugin) and not isinstance(plugin, BaseBatchPlugin)
            )

        return [
            {"id": plugin.id, "name": plugin.plugin_name,
             "selected": self.plugin_selection.get(plugin.id, False)}
            for plugin in self.plugins.values() if is_valid_plugin(plugin)
        ]
