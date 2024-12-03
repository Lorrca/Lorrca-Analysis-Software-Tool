import logging
from matplotlib import pyplot as plt
from src.models.plot_element import PlotElement

logger = logging.getLogger(__name__)


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

    def remove_element(self, element):
        """Remove a specific plot element."""
        if element.id in self.elements:
            del self.elements[element.id]
            logger.info(f"Element {element.id} removed from PlotManager.")
        else:
            logger.warning(f"Element {element.id} not found in PlotManager.")

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

    def visualize_selected_elements(self, selected_element_ids=None):
        """Visualize only selected elements based on provided IDs."""
        self.ax.clear()  # Clear previous plot elements

        if selected_element_ids is None:
            # If no specific IDs are provided, visualize all selected elements
            for element in self.elements.values():
                if element.selected:  # Check if selected
                    element.render(self.ax)
        else:
            # Visualize only the elements whose IDs are in the provided list
            for element_id in selected_element_ids:
                element = self.get_element_by_id(element_id)
                if element and element.selected:  # Check if the element exists and is selected
                    element.render(self.ax)

        self.ax.legend()  # Add a legend for better readability

    def set_element_selection(self, element_id, is_selected):
        """Set the selection state for a given element."""
        element = self.get_element_by_id(element_id)
        if element:
            element.set_selected(is_selected)
            logger.info(
                f"Element {element_id} selection state set to {is_selected}.")
        else:
            logger.warning(f"Element {element_id} not found in PlotManager.")

    def cleanup_plugin_elements(self, plugin_id):
        """Deregister all elements associated with a given plugin ID."""
        self.remove_elements_by_plugin_id(plugin_id)
