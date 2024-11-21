import matplotlib.pyplot as plt
import uuid


class PlotManager:
    def __init__(self):
        """Initialize an empty dictionary to store plot elements."""
        self.elements = {}

    def add_line(self, x, y, label=None, plugin_name=None, **kwargs):
        """Add a line element with an automatically generated unique ID."""
        element_id = str(uuid.uuid4())
        self.elements[element_id] = {
            'type': 'line',
            'x': x,
            'y': y,
            'kwargs': kwargs,
            'label': label,
            'plugin_name': plugin_name,
        }

    def add_point(self, x: float, y: float, label=None, plugin_name=None, **kwargs):
        """Add a single point element with an automatically generated unique ID."""
        element_id = str(uuid.uuid4())
        self.elements[element_id] = {
            'type': 'point',
            'x': x,
            'y': y,
            'kwargs': kwargs,
            'label': label,
            'plugin_name': plugin_name,
        }

    def add_area(self, x, y1, y2, label=None, plugin_name=None, **kwargs):
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
        }

    def add_scatter(self, x, y, label=None, plugin_name=None, **kwargs):
        """Add a scatter plot element with an automatically generated unique ID."""
        element_id = str(uuid.uuid4())
        self.elements[element_id] = {
            'type': 'scatter',
            'x': x,
            'y': y,
            'kwargs': kwargs,
            'label': label,
            'plugin_name': plugin_name,
        }

    def add_histogram(self, data, bins=10, label=None, plugin_name=None, **kwargs):
        """Add a histogram element with an automatically generated unique ID."""
        element_id = str(uuid.uuid4())
        self.elements[element_id] = {
            'type': 'histogram',
            'data': data,
            'bins': bins,
            'kwargs': kwargs,
            'label': label,
            'plugin_name': plugin_name,
        }

    def add_bar(self, x, height, label=None, plugin_name=None, **kwargs):
        """Add a bar chart element with an automatically generated unique ID."""
        element_id = str(uuid.uuid4())
        self.elements[element_id] = {
            'type': 'bar',
            'x': x,
            'height': height,
            'kwargs': kwargs,
            'label': label,
            'plugin_name': plugin_name,
        }

    def get_elements(self):
        """Return the dictionary of all elements."""
        return self.elements

    def visualize_selected_elements(self, element_ids, title="No Title",
                                    x_label="Please Define",
                                    y_label="Please Define"):
        """Visualize elements with a plot title and axis labels."""
        # Clear any existing plots
        plt.close('all')

        # Create a new figure
        plt.figure()

        for element_id in element_ids:
            element = self.elements.get(element_id)
            if element is None:
                continue  # Skip if the element ID does not exist

            element_type = element['type']
            if element_type == 'line':
                plt.plot(element['x'], element['y'], label=element.get('label'),
                         **element['kwargs'])
            elif element_type == 'point':
                plt.plot(element['x'], element['y'], 'o', label=element.get('label'),
                         **element['kwargs'])
            elif element_type == 'area':
                plt.fill_between(element['x'], element['y1'], element['y2'],
                                 label=element.get('label'), **element['kwargs'])
            elif element_type == 'scatter':
                plt.scatter(element['x'], element['y'], label=element.get('label'),
                            **element['kwargs'])
            elif element_type == 'histogram':
                plt.hist(element['data'], bins=element['bins'], label=element.get('label'),
                         **element['kwargs'])
            elif element_type == 'bar':
                plt.bar(element['x'], element['height'], label=element.get('label'),
                        **element['kwargs'])

        # Set the title and axis labels
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend()  # Add a legend for better readability
        plt.show()
