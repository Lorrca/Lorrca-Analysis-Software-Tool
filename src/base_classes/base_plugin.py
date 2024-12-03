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
        self.elements = []  # Local storage for plugin elements

    @property
    @abstractmethod
    def plugin_name(self) -> str:
        """Property for plugin name, to be overridden by subclasses."""
        pass

    def _register_element(self, element):
        """Register an element with the PlotManager and store it locally."""
        self.elements.append(element)
        self.plot_manager.add_element(element)

    def add_line_element(self, x: list, y: list, label: str):
        """Helper method to add a line plot element."""
        element = LineElement(x, y, label, self.plugin_name, self.id)
        self._register_element(element)

    def add_point_element(self, x: float, y: float, label: str):
        """Helper method to add a point plot element."""
        element = ScatterElement([x], [y], label, self.plugin_name, self.id)
        self._register_element(element)

    def add_area_element(self, x: list, y1: list, y2: list, label: str):
        """Helper method to add an area plot element."""
        element = AreaElement(x, y1, y2, label, self.plugin_name, self.id)
        self._register_element(element)

    def remove_element(self, element_id):
        """Remove an element by its ID."""
        element = next((e for e in self.elements if e.id == element_id), None)
        if element:
            self.elements.remove(element)
            self.plot_manager.remove_element(element)
            logger.info(
                f"Element {element_id} removed from plugin {self.plugin_name}."
            )
        else:
            logger.warning(
                f"Element {element_id} not found in plugin {self.plugin_name}."
            )

    def cleanup(self):
        """Deregister all elements from the PlotManager."""
        for element in self.elements:
            self.plot_manager.remove_element(element)
            logger.info(f"Element {element.id} removed from plugin {self.plugin_name}.")
        self.elements.clear()
        logger.info(f"All elements from plugin {self.plugin_name} have been cleaned up.")

    def get_elements(self):
        """Return all elements stored by the plugin."""
        return self.elements

    @abstractmethod
    def run_plugin(self):
        """Method to be implemented by subclasses for plugin-specific logic."""
        pass
