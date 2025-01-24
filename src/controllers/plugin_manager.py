import importlib
import inspect
import logging
import os

from src.base_classes.base_hc_plugin import BaseHCPlugin
from src.base_classes.base_plugin import BasePlugin

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
            logger.warning(f"Plugin folder {PLUGINS_FOLDER} not found.")
            return

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
                    if plugin_instance.id in self.plugins:
                        logger.warning(f"Duplicate plugin ID {plugin_instance.id}. Skipping...")
                        return
                    # Store plugin instance
                    self.plugins[plugin_instance.id] = plugin_instance
                    # Set default selection state to True
                    self.plugin_selection[plugin_instance.id] = True
                    logger.info(f"Loaded plugin {plugin_instance.plugin_name}")
                    return
        except Exception as e:
            logger.error(f"Error loading plugin {plugin_name}: {e}")

    def run_plugin(self, plugin_id):
        """Run the plugin for each selected model."""
        plugin = self.plugins.get(plugin_id)
        if plugin:
            try:
                if isinstance(plugin, BaseHCPlugin):
                    # Run the plugin with the healthy control model
                    plugin.run_plugin(self.model_container.hc_model)
                elif isinstance(plugin, BasePlugin):
                    # Get all selected models
                    selected_models = self.model_container.get_selected_models()
                    if not selected_models:
                        logger.warning("No models selected to run the plugin on.")
                        return

                    # Pass the selected models to the plugin's `run_plugin` method
                    for model in selected_models:
                        plugin.run_plugin(model)

                    logger.info(f"Ran plugin: {plugin.plugin_name} on selected models.")
            except Exception as e:
                logger.error(f"Error running plugin {plugin.plugin_name}: {e}")
        else:
            logger.warning(f"Plugin with ID {plugin_id} not found.")

    def analyze_model(self, model_id):
        """
        Analyzes the specified model by running all available selected plugins on it.

        Args:
        model_id (str): The unique identifier of the model to be analyzed.
        """
        try:
            model = self.model_container.get_model_by_id(model_id)
            if not model:
                logger.warning(f"Model with ID {model_id} not found.")
                return

            for plugin_id, plugin in self.plugins.items():
                if self.plugin_selection.get(plugin_id, False):  # Check if the plugin is selected
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

    def get_plugins(self, hc_plugins=False):
        """
        Return a list of plugins with their selection state.

        :param hc_plugins: If True, return only Healthy Control plugins (BaseHCPlugin).
                           If False, return only standard plugins (BasePlugin excluding BaseHCPlugin).
        """

        def is_valid_plugin(plugin):
            return (
                isinstance(plugin, BaseHCPlugin) if hc_plugins
                else isinstance(plugin, BasePlugin) and not isinstance(plugin, BaseHCPlugin)
            )

        return [
            {"id": plugin.id, "name": plugin.plugin_name,
             "selected": self.plugin_selection.get(plugin.id, False)}
            for plugin in self.plugins.values() if is_valid_plugin(plugin)
        ]
