import logging
import os

from matplotlib import pyplot as plt
from src.models.plot_element import PlotElement
from src.utils.plot_export_helper import save_plot_with_clone

logger = logging.getLogger(__name__)

# Default constants for plot settings
DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1080
DEFAULT_DPI = 200
DEFAULT_X_LABEL = "X Axis"
DEFAULT_Y_LABEL = "Y Axis"
DEFAULT_TITLE = "Plot"
RESULTS_FOLDER = "../results"


class PlotManager:
    def __init__(self):
        """Initialize an empty dictionary to store plot elements."""
        self.elements = {}  # Elements will be stored using their unique IDs
        self.fig, self.ax = plt.subplots()  # Initialize the figure and axis for plotting

    def get_figure(self):
        return self.fig

    def add_element(self, element: PlotElement):
        """Add a plot element to the manager."""
        if not isinstance(element, PlotElement):
            raise TypeError(
                "Only instances of PlotElement (or subclasses) can be added.")
        self.elements[element.id] = element

    def remove_element_by_id(self, element_id):
        """Remove a plot element by its ID."""
        if element_id in self.elements:
            del self.elements[element_id]

    def remove_elements_by_plugin_id(self, plugin_id):
        """Remove all plot elements associated with a given plugin ID."""
        elements_to_remove = [element_id for element_id, element in
                              self.elements.items() if
                              element.plugin_id == plugin_id]
        for element_id in elements_to_remove:
            self.remove_element_by_id(element_id)

    def get_element_by_id(self, element_id):
        """Retrieve a plot element by its ID."""
        return self.elements.get(element_id)

    def get_all_elements(self):
        """Return the dictionary of all elements."""
        return self.elements

    def _set_elements_state(self, selected_element_ids):
        # Iterate through all elements and set their state
        for element_id, element in self.get_all_elements().items():  # Corrected to iterate over items
            if element_id in selected_element_ids:
                element.selected = True
            else:
                element.selected = False

    def visualize_selected_elements(self, selected_element_ids):
        """Visualize only selected elements based on provided IDs."""
        self.ax.clear()  # Clear previous plot elements

        # Update the state of all elements
        self._set_elements_state(selected_element_ids)

        # Visualize only the elements whose IDs are in the provided list and are marked as selected
        for element_id in selected_element_ids:
            element = self.get_element_by_id(element_id)
            if element and element.selected:  # Check if the element exists and is selected
                element.render(self.ax)

        self.ax.legend()  # Add a legend for better readability

    def save_plot(self, filename, width, height, dpi, x_label, y_label, title):
        """Export the plot as an image with the specified parameters."""
        try:
            # Ensure the results folder exists
            os.makedirs(RESULTS_FOLDER, exist_ok=True)

            # Ensure the filename is stored in the results folder
            filepath = os.path.join(RESULTS_FOLDER, filename + ".png")

            # Save the plot using the helper function
            save_plot_with_clone(self.fig, filename=filepath, width=width, height=height, dpi=dpi,
                                 x_label=x_label, y_label=y_label, title=title
                                 )

            logger.info(f"Plot saved successfully as {filepath}")
        except Exception as e:
            logger.error(f"Failed to save plot: {e}")
            raise
