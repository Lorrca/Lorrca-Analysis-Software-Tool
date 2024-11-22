import uuid
from abc import ABC, abstractmethod

from src.interfaces.plugin_interface import PluginInterface


class BasePlugin(PluginInterface, ABC):
    __slots__ = "model", "plot_manager", "plugin_id"

    def __init__(self, model, plot_manager):
        super().__init__(model, plot_manager)
        self.model = model
        self.plot_manager = plot_manager
        self.plugin_id = str(uuid.uuid4())

    @property
    @abstractmethod
    def plugin_name(self):
        """
        Each derived plugin must define its name.
        This property ensures the name is available without duplication.
        """
        pass

    def add_line_element(self, x, y, label):
        """Helper to add a line plot with the plugin's name."""
        self.plot_manager.add_line(x, y, label, self.plugin_name, self.plugin_id)

    def add_point_element(self, x, y, label):
        """Helper to add a point plot with the plugin's name."""
        self.plot_manager.add_point(x, y, label, self.plugin_name, self.plugin_id)

    def add_area_element(self, x, y1, y2, label):
        """Helper to add an area plot with the plugin's name."""
        self.plot_manager.add_area(x, y1, y2, label, self.plugin_name, self.plugin_id)

    @abstractmethod
    def run_plugin(self):
        """Override in derived classes to implement the plugin logic."""
        pass
