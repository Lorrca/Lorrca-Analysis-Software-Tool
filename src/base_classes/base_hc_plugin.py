from abc import abstractmethod, ABC

from src.base_classes.base_plugin import BasePlugin, UnionList
from src.models.hc_model import HCModel
from src.models.plot_element import LineElement, AreaElement, ScatterElement, CompositeLineElement


class BaseHCPlugin(BasePlugin, ABC):
    @abstractmethod
    def run_plugin(self, model: HCModel):
        """Method to be implemented by subclasses for plugin-specific logic."""
        pass

    def add_line_element(self, x: UnionList, y: UnionList, label: str, **kwargs):
        """Helper method to add a line plot element."""
        element = LineElement(x, y, label, self, self.model, **kwargs)
        element.is_hc = True
        self.plot_manager.add_element(element)

    def add_point_element(self, x: float, y: float, label: str, **kwargs):
        """Helper method to add a point plot element."""
        element = ScatterElement([x], [y], label, self, self.model, **kwargs)
        element.is_hc = True
        self.plot_manager.add_element(element)

    def add_area_element(self, x: UnionList, y1: UnionList, y2: UnionList, label: str, **kwargs):
        """Helper method to add an area plot element."""
        kwargs.setdefault("alpha", 0.5)  # Set default alpha to 0.5 if not provided
        element = AreaElement(x, y1, y2, label, self, self.model, **kwargs)
        element.is_hc = True
        self.plot_manager.add_element(element)

    def add_composite_line_element(self, lines: list[tuple], label: str, **kwargs):
        """
        Helper method to add a composite line plot element.
        """
        element = CompositeLineElement(lines, label, self, self.model, **kwargs)
        element.is_hc = True
        self.plot_manager.add_element(element)
