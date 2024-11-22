import os
import importlib.util


class PluginManager:
    def __init__(self, model, plotter, plugin_folder):
        """
        Initialize the PluginManager with the model, plotter, and plugin folder.
        """
        self.model = model
        self.plotter = plotter
        self.plugin_folder = plugin_folder
        self.discovered_plugins = []  # Store discovered plugin names
        self.used_plugins = []

    def scan_plugins(self):
        if not os.path.isdir(self.plugin_folder):
            print(f"Plugin folder '{self.plugin_folder}' does not exist.")
            return

        self.discovered_plugins = []
        for filename in os.listdir(self.plugin_folder):
            if filename.endswith("_plugin.py"):
                plugin_name = filename[:-3]
                self.discovered_plugins.append(plugin_name)

        print(f"Discovered plugins: {self.discovered_plugins}")  # Debugging line to check plugins

    def load_plugin(self, plugin_name):
        """
        Load a plugin module by its name.
        Returns the loaded module or None if loading fails.
        """
        plugin_path = os.path.join(self.plugin_folder, f"{plugin_name}.py")

        if not os.path.isfile(plugin_path):
            print(f"Plugin '{plugin_name}' not found.")
            return None

        try:
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            plugin_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin_module)
            self.used_plugins.append(plugin_module)
            return plugin_module
        except Exception as error:
            print(f"Failed to load plugin '{plugin_name}': {error}")
            return None

    def run_selected_plugins(self, selected_plugins):
        """
        Run the selected plugins by their names.
        Each plugin must define a 'run_plugin' function.
        """
        for plugin_name in selected_plugins:
            if plugin_name not in self.discovered_plugins:
                print(f"Plugin '{plugin_name}' is not recognized.")
                continue

            # Dynamically load the plugin
            plugin_module = self.load_plugin(plugin_name)
            if not plugin_module:
                continue

            # Execute the 'run_plugin' function if it exists
            if hasattr(plugin_module, "run_plugin"):
                print(f"Running plugin: {plugin_name}")
                try:
                    plugin_module.run_plugin(self.model, self.plotter)
                except Exception as error:
                    print(f"Error while running plugin '{plugin_name}': {error}")
            else:
                print(f"Plugin '{plugin_name}' does not have a 'run_plugin' function.")
