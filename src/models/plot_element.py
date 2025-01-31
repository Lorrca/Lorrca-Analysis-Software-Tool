import uuid
from abc import ABC, abstractmethod


# Base class for plot elements
class PlotElement(ABC):
    def __init__(self, label: str, plugin, model, **kwargs):
        self.id = str(uuid.uuid4())  # Generate a unique ID for each element
        self.label = label
        self.plugin = plugin
        self.model = model
        self.kwargs = kwargs
        self.is_batch = False  # True for batch plugin' elements
        self.is_reference = False  # True if used as a reference in the background

    @abstractmethod
    def render(self, ax):
        """Subclasses must implement the render method to plot the element."""
        pass

    def get_render_kwargs(self, color=None):
        """Returns the keyword arguments for rendering, applying reference styling if necessary."""
        kwargs = self.kwargs.copy()

        if self.is_reference:
            kwargs.setdefault("color", "grey")  # Default to grey for reference elements
            kwargs.setdefault("zorder", -1)  # Ensure it renders in the background
            kwargs.setdefault("alpha", 0.5)  # Reduce opacity for clarity
        elif color is not None:  # If not a reference, apply the color from PlotManager
            kwargs["color"] = color

        return kwargs

    @property
    def model_name(self):
        """Return the name of the model."""
        return self.model.name if self.model else "Failed to Load Model Name"

    @property
    def plugin_name(self):
        """Return the name of the plugin."""
        return self.plugin.plugin_name if self.plugin else "Failed to Load Plugin Name"

    @property
    def model_id(self):
        """Return the name of the model."""
        return self.model.id

    @property
    def plugin_id(self):
        """Return the name of the plugin."""
        return self.plugin.id


# Line plot element
class LineElement(PlotElement):
    def __init__(self, x, y, label, plugin, model, **kwargs):
        super().__init__(label, plugin, model, **kwargs)
        self.x = x
        self.y = y

    def render(self, ax, color=None):
        ax.plot(self.x, self.y, label=self.label, **self.get_render_kwargs(color))


# Area plot element
class AreaElement(PlotElement):
    def __init__(self, x, y1, y2, label, plugin, model, **kwargs):
        super().__init__(label, plugin, model, **kwargs)
        self.x = x
        self.y1 = y1
        self.y2 = y2

    def render(self, ax, color=None):
        ax.fill_between(self.x, self.y1, self.y2, label=self.label, **self.get_render_kwargs(color))


# Scatter plot element
class ScatterElement(PlotElement):
    def __init__(self, x, y, label, plugin, model, **kwargs):
        super().__init__(label, plugin, model, **kwargs)
        self.x = x
        self.y = y

    def render(self, ax, color=None):
        ax.scatter(self.x, self.y, label=self.label, **self.get_render_kwargs(color))


# Composite Line plot element
class CompositeLineElement(PlotElement):
    def __init__(self, lines: list[tuple], label, plugin, model, **kwargs):
        super().__init__(label, plugin, model, **kwargs)
        self.lines = lines

    def render(self, ax, color=None):
        kwargs = self.get_render_kwargs(color)
        for i, (x, y) in enumerate(self.lines):
            line_kwargs = kwargs.copy()
            line_kwargs["label"] = self.label if i == 0 else "_nolegend_"
            ax.plot(x, y, **line_kwargs)
