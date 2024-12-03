import importlib
import logging
import os
from src.base_classes.base_plugin import BasePlugin

PLUGINS_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                              '../plugins')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PluginManager:
    def __init__(self, plugins_folder=PLUGINS_FOLDER):
        self.plugins = {}
        self.plugins_folder = plugins_folder

    def load_plugins(self, model, plot_manager):
        if not os.path.isdir(self.plugins_folder):
            logger.warning(f"Plugin folder {self.plugins_folder} not found.")
            return

        for file_name in os.listdir(self.plugins_folder):
            if file_name.endswith(".py") and file_name != "__init__.py":
                plugin_name = file_name[:-3]
                self._load_plugin(plugin_name, model, plot_manager)

    def _load_plugin(self, plugin_name, model, plot_manager):
        try:
            plugin_module = importlib.import_module(f"plugins.{plugin_name}")
            for attr_name in dir(plugin_module):
                attr = getattr(plugin_module, attr_name)
                if isinstance(attr, type) and issubclass(attr,
                                                         BasePlugin) and attr is not BasePlugin:
                    plugin_instance = attr(model, plot_manager)
                    if plugin_instance.id in self.plugins:
                        logger.warning(
                            f"Duplicate plugin ID {plugin_instance.id}. Skipping...")
                        return
                    self.plugins[plugin_instance.id] = plugin_instance
                    logger.info(f"Loaded plugin {plugin_instance.plugin_name}")
                    return
        except Exception as e:
            logger.error(f"Error loading plugin {plugin_name}: {e}")

    def run_plugin(self, plugin_id):
        plugin = self.plugins.get(plugin_id)
        if plugin:
            try:
                # Run the plugin
                plugin.run_plugin()

                logger.info(f"Ran plugin: {plugin.plugin_name}")
            except Exception as e:
                logger.error(f"Error running plugin {plugin.plugin_name}: {e}")
        else:
            logger.warning(f"Plugin with ID {plugin_id} not found.")

    def get_all_plugin_info(self):
        """Return a list of dictionaries containing plugin IDs and names."""
        return [{"id": plugin.id, "name": plugin.plugin_name} for plugin in
                self.plugins.values()]

    def get_plugin_by_id(self, plugin_id):
        """Return the plugin object by its ID."""
        return self.plugins.get(plugin_id)
