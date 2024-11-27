import uuid
from abc import (abstractmethod)
from src.interfaces.plugin_interface import PluginInterface


class BasePlugin(PluginInterface):
    """Base class for all plugins."""

    def __init__(self, model, plot_manager):
        super().__init__(model, plot_manager)
        self.model = model
        self.plot_manager = plot_manager
        self.plugin_id = str(uuid.uuid4())  # Unique ID for each plugin
        self.run_status = False  # Track if the plugin has been run

    @property
    @abstractmethod
    def plugin_name(self) -> str:
        """Property for plugin name, to be overridden by subclasses."""
        pass  # Subclasses must implement the plugin name.

    def add_line_element(self, x: list, y: list, label: str):
        """Helper method to add a line plot element."""
        self.plot_manager.add_line(x, y, label, self.plugin_name, self.plugin_id)

    def add_point_element(self, x: float, y: float, label: str):
        """Helper method to add a point plot element."""
        self.plot_manager.add_point(x, y, label, self.plugin_name, self.plugin_id)

    def add_area_element(self, x: list, y1: list, y2: list, label: str):
        """Helper method to add an area plot element."""
        self.plot_manager.add_area(x, y1, y2, label, self.plugin_name, self.plugin_id)

    def reset(self):
        """Reset the plugin's run status."""
        self.run_status = False

    @abstractmethod
    def run_plugin(self):
        """Method to be implemented by subclasses for plugin-specific logic."""
        pass
