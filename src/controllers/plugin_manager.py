import importlib
import logging
import os

from src.base_classes.base_plugin import BasePlugin

PLUGINS_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                              '../plugins')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PluginManager:
    def __init__(self, model_container):
        self.model_container = model_container
        self.plugins = {}

    def load_plugins(self, plot_manager):
        """Loads all plugins from the plugins folder."""
        if not os.path.isdir(PLUGINS_FOLDER):
            logger.warning(f"Plugin folder {PLUGINS_FOLDER} not found.")
            return

        for file_name in os.listdir(PLUGINS_FOLDER):
            if file_name.endswith(".py") and file_name != "__init__.py":
                plugin_name = file_name[:-3]
                self._load_plugin(plugin_name, plot_manager)

    def _load_plugin(self, plugin_name, plot_manager):
        """Loads a single plugin by its name."""
        try:
            plugin_module = importlib.import_module(f"plugins.{plugin_name}")
            for attr_name in dir(plugin_module):
                attr = getattr(plugin_module, attr_name)
                if isinstance(attr, type) and issubclass(attr,
                                                         BasePlugin) and attr is not BasePlugin:
                    plugin_instance = attr(plot_manager)
                    if plugin_instance.id in self.plugins:
                        logger.warning(f"Duplicate plugin ID {plugin_instance.id}. Skipping...")
                        return
                    self.plugins[plugin_instance.id] = plugin_instance
                    logger.info(f"Loaded plugin {plugin_instance.plugin_name}")
                    return
        except Exception as e:
            logger.error(f"Error loading plugin {plugin_name}: {e}")

    def run_plugin(self, plugin_id):
        """Run the plugin for each selected model."""
        plugin = self.plugins.get(plugin_id)
        if plugin:
            try:
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
        try:
            model = self.model_container.get_model_by_id(model_id)
            if not model:
                logger.warning(f"Model with ID {model_id} not found.")
                return

            for _, plugin in self.plugins.items():
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
        """Return a list of dictionaries containing plugin IDs and names."""
        return [{"id": plugin.id, "name": plugin.plugin_name} for plugin in self.plugins.values()]

    def get_plugin_by_id(self, plugin_id):
        """Return the plugin object by its ID."""
        return self.plugins.get(plugin_id)
