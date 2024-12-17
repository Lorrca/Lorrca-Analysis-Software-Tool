import logging
import uuid
from abc import ABC, abstractmethod
from typing import Union

import numpy as np

from src.models.plot_element import LineElement, AreaElement, ScatterElement

logger = logging.getLogger(__name__)

UnionList = Union[list, np.ndarray]


class BasePlugin(ABC):
    """Base class for all plugins."""

    def __init__(self, plot_manager):
        self.model = None
        self.plot_manager = plot_manager
        self.id = str(uuid.uuid4())

    @property
    @abstractmethod
    def plugin_name(self) -> str:
        """Property for plugin name, to be overridden by subclasses."""
        pass

    def add_line_element(self, x: UnionList, y: UnionList, label: str,
                         **kwargs):
        """Helper method to add a line plot element."""
        element = LineElement(x, y, label, self.plugin_name, self.id, **kwargs)
        self.plot_manager.add_element(element)

    def add_point_element(self, x: float, y: float, label: str, **kwargs):
        """Helper method to add a point plot element."""
        element = ScatterElement([x], [y], label, self.plugin_name, self.id, **kwargs)
        self.plot_manager.add_element(element)

    def add_area_element(self, x: UnionList, y1: UnionList,
                         y2: UnionList, label: str, **kwargs):
        """Helper method to add an area plot element."""
        kwargs.setdefault("alpha", 0.5)  # Set default alpha to 0.5 if not provided
        element = AreaElement(x, y1, y2, label, self.plugin_name, self.id, **kwargs)
        self.plot_manager.add_element(element)

    @abstractmethod
    def run_plugin(self, model):
        """Method to be implemented by subclasses for plugin-specific logic."""
        pass
