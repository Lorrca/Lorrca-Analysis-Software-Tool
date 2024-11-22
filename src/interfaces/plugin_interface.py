from abc import ABC, abstractmethod


class PluginInterface(ABC):
    def __init__(self, model, plot_manager):
        """Initialize the PluginInterface with a model and a plotting object."""
        super().__init__()
        self.model = model
        self.plot_manager = plot_manager

    @abstractmethod
    def run_plugin(self):
        """Run the plugin's functionality."""
        pass

    @abstractmethod
    def get_plugin_name(self) -> str:
        """Return the name of the plugin."""
        pass
