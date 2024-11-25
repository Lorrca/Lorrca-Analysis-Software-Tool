import matplotlib.pyplot as plt
import uuid


class PlotManager:
    __slots__ = "elements", "fig", "ax"

    def __init__(self):
        """Initialize an empty dictionary to store plot elements."""
        self.elements = {}
        self.fig, self.ax = plt.subplots()  # Initialize the figure and axis for plotting

    def get_figure(self):
        return self.fig

    def add_line(self, x, y, label: str, plugin_name: str, plugin_id, **kwargs):
        """Add a line element with an automatically generated unique ID."""
        element_id = str(uuid.uuid4())
        self.elements[element_id] = {
            'type': 'line',
            'x': x,
            'y': y,
            'kwargs': kwargs,
            'label': label,
            'plugin_name': plugin_name,
            "plugin_id": plugin_id
        }

    def add_point(self, x: float, y: float, label: str, plugin_name: str, plugin_id, **kwargs):
        """Add a single point element with an automatically generated unique ID."""
        element_id = str(uuid.uuid4())
        self.elements[element_id] = {
            'type': 'point',
            'x': x,
            'y': y,
            'kwargs': kwargs,
            'label': label,
            'plugin_name': plugin_name,
            "plugin_id": plugin_id
        }

    def add_area(self, x, y1, y2, label: str, plugin_name: str, plugin_id, **kwargs):
        """Add an area fill element with an automatically generated unique ID."""
        element_id = str(uuid.uuid4())
        self.elements[element_id] = {
            'type': 'area',
            'x': x,
            'y1': y1,
            'y2': y2,
            'kwargs': kwargs,
            'label': label,
            'plugin_name': plugin_name,
            "plugin_id": plugin_id
        }

    def add_scatter(self, x, y, label: str, plugin_name: str, plugin_id, **kwargs):
        """Add a scatter plot element with an automatically generated unique ID."""
        element_id = str(uuid.uuid4())
        self.elements[element_id] = {
            'type': 'scatter',
            'x': x,
            'y': y,
            'kwargs': kwargs,
            'label': label,
            'plugin_name': plugin_name,
            "plugin_id": plugin_id
        }

    def add_histogram(self, data, bins, label: str, plugin_name: str, plugin_id, **kwargs):
        """Add a histogram element with an automatically generated unique ID."""
        element_id = str(uuid.uuid4())
        self.elements[element_id] = {
            'type': 'histogram',
            'data': data,
            'bins': bins,
            'kwargs': kwargs,
            'label': label,
            'plugin_name': plugin_name,
            "plugin_id": plugin_id
        }

    def add_bar(self, x, height, label: str, plugin_name: str, plugin_id, **kwargs):
        """Add a bar chart element with an automatically generated unique ID."""
        element_id = str(uuid.uuid4())
        self.elements[element_id] = {
            'type': 'bar',
            'x': x,
            'height': height,
            'kwargs': kwargs,
            'label': label,
            'plugin_name': plugin_name,
            "plugin_id": plugin_id
        }

    def get_all_elements(self):
        """Return the dictionary of all elements."""
        return self.elements

    def get_elements_by_plugin_id(self, plugin_id):
        """Returns the dictionary of elements created by a specific plugin."""
        return {
            key: val for key, val in self.elements.items()
            if (plugin_id and val["plugin_id"] == plugin_id)
        }

    def remove_plugin_elements(self, plugin_id):
        """Removes all elements created by a specific plugin ID."""
        if not plugin_id:
            return  # Do nothing if no plugin ID is provided

        # Use dictionary comprehension to filter out elements created by the plugin
        self.elements = {
            key: val for key, val in self.elements.items()
            if val["plugin_id"] != plugin_id
        }

    def visualize_selected_elements(self, element_ids):
        """Visualize elements with a plot title and axis labels."""
        # Clear previous plot elements
        self.ax.clear()

        # Add the selected elements
        for element_id in element_ids:
            element = self.elements.get(element_id)
            if element is None:
                continue  # Skip if the element ID does not exist

            element_type = element['type']
            if element_type == 'line':
                self.ax.plot(element['x'], element['y'], label=element.get('label'),
                             **element['kwargs'])
            elif element_type == 'point':
                self.ax.plot(element['x'], element['y'], 'o', label=element.get('label'),
                             **element['kwargs'])
            elif element_type == 'area':
                self.ax.fill_between(element['x'], element['y1'], element['y2'],
                                     label=element.get('label'), **element['kwargs'])
            elif element_type == 'scatter':
                self.ax.scatter(element['x'], element['y'], label=element.get('label'),
                                **element['kwargs'])
            elif element_type == 'histogram':
                self.ax.hist(element['data'], bins=element['bins'], label=element.get('label'),
                             **element['kwargs'])
            elif element_type == 'bar':
                self.ax.bar(element['x'], element['height'], label=element.get('label'),
                            **element['kwargs'])

        self.ax.legend()  # Add a legend for better readability
