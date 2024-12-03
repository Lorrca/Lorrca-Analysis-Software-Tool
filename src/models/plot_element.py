import uuid
from abc import ABC, abstractmethod


# Base class for plot elements
class PlotElement(ABC):
    def __init__(self, label: str, plugin_name: str, plugin_id, **kwargs):
        self.id = str(uuid.uuid4())  # Generate a unique ID for each element
        self.label = label
        self.plugin_name = plugin_name
        self.plugin_id = plugin_id
        self.kwargs = kwargs
        self.selected = True  # Default to selected

    @abstractmethod
    def render(self, ax):
        """Subclasses must implement the render method to plot the element."""
        pass

    def set_selected(self, is_selected):
        """Set the selection state of the element."""
        self.selected = is_selected


# Line plot element
class LineElement(PlotElement):
    def __init__(self, x, y, label, plugin_name, plugin_id, **kwargs):
        super().__init__(label, plugin_name, plugin_id, **kwargs)
        self.x = x
        self.y = y

    def render(self, ax):
        ax.plot(self.x, self.y, label=self.label, **self.kwargs)


# Area plot element
class AreaElement(PlotElement):
    def __init__(self, x, y1, y2, label, plugin_name, plugin_id, **kwargs):
        super().__init__(label, plugin_name, plugin_id, **kwargs)
        self.x = x
        self.y1 = y1
        self.y2 = y2

    def render(self, ax):
        ax.fill_between(self.x, self.y1, self.y2, label=self.label,
                        **self.kwargs)


# Scatter plot element
class ScatterElement(PlotElement):
    def __init__(self, x, y, label, plugin_name, plugin_id, **kwargs):
        super().__init__(label, plugin_name, plugin_id, **kwargs)
        self.x = x
        self.y = y

    def render(self, ax):
        ax.scatter(self.x, self.y, label=self.label, **self.kwargs)
