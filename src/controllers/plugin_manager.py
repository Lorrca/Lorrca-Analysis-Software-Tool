import importlib
import os

from src.base_classes.base_plugin import BasePlugin

PLUGINS_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../plugins')


class PluginManager:
    def __init__(self, model, plot_manager):
        self.model = model
        self.plot_manager = plot_manager
        self.plugin_folder = PLUGINS_FOLDER
        self.plugins = {}

    def load_plugins(self):
        """Load all plugins from the specified folder."""
        if not os.path.isdir(self.plugin_folder):
            print(f"Plugin folder {self.plugin_folder} not found.")
            return

        for file_name in os.listdir(self.plugin_folder):
            if file_name.endswith(".py") and file_name != "__init__.py":
                plugin_name = file_name[:-3]
                self._load_plugin(plugin_name)

    def _load_plugin(self, plugin_name):
        """Dynamically import and instantiate the plugin."""
        try:
            plugin_module = importlib.import_module(f"plugins.{plugin_name}")
            for attr_name in dir(plugin_module):
                attr = getattr(plugin_module, attr_name)
                if isinstance(attr, type) and issubclass(attr,
                                                         BasePlugin) and attr is not BasePlugin:
                    plugin_instance = attr(self.model, self.plot_manager)
                    self.plugins[plugin_instance.id] = plugin_instance
                    return
        except Exception as e:
            print(f"Error loading plugin {plugin_name}: {e}")

    def run_plugin(self, plugin_id):
        """Run the plugin if it hasn't been run before."""
        plugin = self.plugins.get(plugin_id)
        if plugin:
            try:
                plugin.run_plugin()
                print(f"Ran plugin: {plugin.plugin_name}")
            except Exception as e:
                print(f"Error running plugin {plugin.plugin_name}: {e}")
        else:
            print(f"Plugin with ID {plugin_id} not found.")

    def get_all_plugin_info(self):
        """Return a list of dictionaries containing plugin IDs and names."""
        return [
            {"id": plugin.id, "name": plugin.plugin_name}
            for plugin in self.plugins.values()
        ]

    def get_plugin_by_id(self, plugin_id):
        """Return the plugin object by its ID."""
        return self.plugins.get(plugin_id)