import itertools
import logging
import os

from matplotlib import pyplot as plt
from src.models.plot_element import PlotElement
from src.utils.plot_export_helper import save_plot_with_clone

logger = logging.getLogger(__name__)

RESULTS_FOLDER = "../results"


class PlotManager:
    def __init__(self):
        """Initialize an empty dictionary to store plot elements."""
        self.elements = {}  # Store plot elements by their unique ID
        self.fig, self.ax = plt.subplots()  # Initialize the figure and axis for plotting
        plt.ion()  # Enable interactive mode

    def get_figure(self):
        """Return the figure object for external manipulation."""
        return self.fig

    def add_element(self, element: PlotElement):
        """Add a plot element to the manager."""
        if not isinstance(element, PlotElement):
            raise TypeError(
                "Only instances of PlotElement (or its subclasses) can be added."
            )
        # Use the element's ID as the dictionary key
        self.elements[element.id] = element

    def remove_element_by_id(self, element_id):
        """Remove a plot element by its ID."""
        if element_id in self.elements:
            del self.elements[element_id]

    def get_elements_by_model_id(self, model_id):
        elements_selection = [element for element in self.elements.values() if
                              element.model_id == model_id]
        return elements_selection

    def remove_elements_by_model_id(self, model_id):
        """Remove all plot elements associated with a given model ID."""
        elements_to_remove = [element_id for element_id, element in self.elements.items() if
                              element.model_id == model_id]
        logger.info(f"Elements to be removed: {elements_to_remove}")
        for element_id in elements_to_remove:
            self.remove_element_by_id(element_id)
        logger.info(f"Remaining elements: {self.elements}")

    def remove_elements_by_plugin_id(self, plugin_id):
        """Remove all plot elements associated with a given model ID."""
        elements_to_remove = [element_id for element_id, element in self.elements.items() if
                              element.plugin_id == plugin_id]
        logger.info(f"Elements to be removed: {elements_to_remove}")
        for element_id in elements_to_remove:
            self.remove_element_by_id(element_id)
        logger.info(f"Remaining elements: {self.elements}")

    def get_element_by_id(self, element_id):
        """Retrieve a plot element by its ID."""
        return self.elements.get(element_id)

    def get_all_elements(self):
        """Return all elements in the manager."""
        return self.elements

    def visualize_selected_elements(self, selected_element_ids):
        """Visualize all selected elements."""
        # Store the current state of the title, and labels
        title = self.ax.get_title()
        x_label = self.ax.get_xlabel()
        y_label = self.ax.get_ylabel()

        self.ax.clear()

        # Get default color cycle
        color_cycle = itertools.cycle(plt.rcParams["axes.prop_cycle"].by_key()["color"])

        # Collect elements that should be rendered
        elements_to_render = [self.get_element_by_id(eid) for eid in selected_element_ids if
                              self.get_element_by_id(eid)]

        # Always render HC elements
        always_visible_elements = [element for element in self.elements.values() if
                                   element.is_batch]

        # Store colors for elements
        element_colors = {}

        # Render all elements with assigned colors
        for element in elements_to_render + always_visible_elements:
            if element not in element_colors:
                element_colors[element] = next(color_cycle)  # Assign unique color

            element.render(self.ax, color=element_colors[element])  # Pass color to render

        # Reapply the title, labels, and grid state
        self.ax.set_title(title)
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.ax.grid(True)

        # Add a legend only if there are any plot elements
        if self.ax.has_data():
            self.ax.legend()  # Add a legend for better readability

    def save_plot(self, filename, width, height, dpi, x_label, y_label, title, grid):
        """Export the plot as an image with the specified parameters."""
        try:
            # Ensure the results folder exists
            os.makedirs(RESULTS_FOLDER, exist_ok=True)

            # Construct the file path to save the plot
            filepath = os.path.join(RESULTS_FOLDER, filename + ".png")

            # Save the plot using the helper function
            save_plot_with_clone(self.fig, filename=filepath, width=width, height=height, dpi=dpi,
                                 x_label=x_label, y_label=y_label, title=title, grid=grid)

            logger.info(f"Plot saved successfully as {filepath}")
        except Exception as e:
            logger.error(f"Failed to save plot: {e}")
            raise
