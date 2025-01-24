import uuid
from abc import ABC, abstractmethod

from matplotlib.colors import LinearSegmentedColormap


# Base class for plot elements
class PlotElement(ABC):
    def __init__(self, label: str, plugin, model, **kwargs):
        self.id = str(uuid.uuid4())  # Generate a unique ID for each element
        self.label = label
        self.plugin = plugin
        self.model = model
        self.kwargs = kwargs

    @abstractmethod
    def render(self, ax):
        """Subclasses must implement the render method to plot the element."""
        pass

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

    def render(self, ax):
        ax.plot(self.x, self.y, label=self.label, **self.kwargs)


# Area plot element
class AreaElement(PlotElement):
    def __init__(self, x, y1, y2, label, plugin, model, **kwargs):
        super().__init__(label, plugin, model, **kwargs)
        self.x = x
        self.y1 = y1
        self.y2 = y2

    def render(self, ax):
        ax.fill_between(self.x, self.y1, self.y2, label=self.label,
                        **self.kwargs)


# Scatter plot element
class ScatterElement(PlotElement):
    def __init__(self, x, y, label, plugin, model, **kwargs):
        super().__init__(label, plugin, model, **kwargs)
        self.x = x
        self.y = y

    def render(self, ax):
        ax.scatter(self.x, self.y, label=self.label, **self.kwargs)


class CompositeLineElement(PlotElement):
    def __init__(self, lines: list[tuple], label, plugin, model, **kwargs):
        super().__init__(label, plugin, model, **kwargs)
        self.lines = lines

        # Create a pastel rainbow color map
        self.cmap = LinearSegmentedColormap.from_list("pastel_rainbow",
                                                     ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF"])

    def render(self, ax):
        num_lines = len(self.lines)

        for i, (x, y) in enumerate(self.lines):
            # Calculate the color based on the line index for smooth transition
            color = self.cmap(i / num_lines)  # Normalize to [0, 1] for the gradient effect

            kwargs = self.kwargs.copy()
            kwargs["color"] = color
            kwargs["zorder"] = -1  # Always render in the background

            if i == 0:
                kwargs["label"] = self.label
            else:
                kwargs["label"] = "_nolegend_"

            ax.plot(x, y, **kwargs)
