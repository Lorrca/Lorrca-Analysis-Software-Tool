import logging
import uuid
from abc import ABC, abstractmethod
from typing import Union

import numpy as np

from src.base_classes.base_scan_model import BaseScanModel
from src.models.plot_element import LineElement, AreaElement, ScatterElement, CompositeLineElement

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
        pass

    def set_model(self, model):
        self.model = model

    def add_line_element(self, x: UnionList, y: UnionList, label: str, is_batch=False,
                         is_reference=False, **kwargs):
        """Helper method to add a line plot element."""
        element = LineElement(x, y, label, self, self.model, **kwargs)
        element.is_batch = is_batch
        element.is_reference = is_reference
        self.plot_manager.add_element(element)

    def add_point_element(self, x: float, y: float, label: str, is_batch=False,
                          is_reference=False, **kwargs):
        """Helper method to add a point plot element."""
        element = ScatterElement([x], [y], label, self, self.model, **kwargs)
        element.is_batch = is_batch
        element.is_reference = is_reference
        self.plot_manager.add_element(element)

    def add_area_element(self, x: UnionList, y1: UnionList, y2: UnionList, label: str,
                         is_batch=False, is_reference=False, **kwargs):
        """Helper method to add an area plot element."""
        kwargs.setdefault("alpha", 0.5)  # Default transparency
        element = AreaElement(x, y1, y2, label, self, self.model, **kwargs)
        element.is_batch = is_batch
        element.is_reference = is_reference
        self.plot_manager.add_element(element)

    def add_composite_line_element(self, lines: list[tuple], label: str, is_batch=False,
                                   is_reference=False, **kwargs):
        """Helper method to add a composite line plot element."""
        element = CompositeLineElement(lines, label, self, self.model, **kwargs)
        element.is_batch = is_batch
        element.is_reference = is_reference
        self.plot_manager.add_element(element)

    @abstractmethod
    def run_plugin(self, model: BaseScanModel):
        pass
