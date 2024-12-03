import logging
import uuid
from abc import ABC, abstractmethod
from src.models.plot_element import LineElement, AreaElement, ScatterElement

logger = logging.getLogger(__name__)


class BasePlugin(ABC):
    """Base class for all plugins."""

    def __init__(self, model, plot_manager):
        self.model = model
        self.plot_manager = plot_manager
        self.id = str(uuid.uuid4())

    @property
    @abstractmethod
    def plugin_name(self) -> str:
        """Property for plugin name, to be overridden by subclasses."""
        pass

    def add_line_element(self, x: list, y: list, label: str):
        """Helper method to add a line plot element."""
        element = LineElement(x, y, label, self.plugin_name, self.id)
        self.plot_manager.add_element(element)

    def add_point_element(self, x: float, y: float, label: str):
        """Helper method to add a point plot element."""
        element = ScatterElement([x], [y], label, self.plugin_name, self.id)
        self.plot_manager.add_element(element)

    def add_area_element(self, x: list, y1: list, y2: list, label: str):
        """Helper method to add an area plot element."""
        element = AreaElement(x, y1, y2, label, self.plugin_name, self.id)
        self.plot_manager.add_element(element)

    def cleanup(self):
        """Remove all elements associated with this plugin from the PlotManager."""
        removed_count = self.plot_manager.remove_elements_by_plugin_id(self.id)
        logger.info(
            f"Removed {removed_count} elements for plugin {self.plugin_name}."
        )

    @abstractmethod
    def run_plugin(self):
        """Method to be implemented by subclasses for plugin-specific logic."""
        pass
