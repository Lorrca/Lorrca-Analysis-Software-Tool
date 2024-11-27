from matplotlib import pyplot as plt

from src.models.plot_element import PlotElement


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
            raise TypeError("Only instances of PlotElement (or subclasses) can be added.")
        self.elements[element.id] = element

    def remove_element_by_id(self, element_id):
        """Remove a plot element by its ID."""
        if element_id in self.elements:
            del self.elements[element_id]

    def remove_elements_by_plugin_id(self, plugin_id):
        """Remove all plot elements associated with a given plugin ID."""
        elements_to_remove = [element_id for element_id, element in self.elements.items() if element.plugin_id == plugin_id]
        for element_id in elements_to_remove:
            self.remove_element_by_id(element_id)

    def get_element_by_id(self, element_id):
        """Retrieve a plot element by its ID."""
        return self.elements.get(element_id)

    def get_all_elements(self):
        """Return the dictionary of all elements."""
        return self.elements

    def visualize_selected_elements(self, element_ids):
        """Visualize elements with a plot title and axis labels."""
        # Clear previous plot elements
        self.ax.clear()

        # Add the selected elements
        for element_id in element_ids:
            element = self.get_element_by_id(element_id)
            if element is None:
                continue  # Skip if the element ID does not exist

            # Render the element on the axis
            element.render(self.ax)

        self.ax.legend()  # Add a legend for better readability
        self.fig.canvas.draw()  # Redraw the canvas to reflect changes
