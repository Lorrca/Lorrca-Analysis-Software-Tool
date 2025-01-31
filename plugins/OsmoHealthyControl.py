import numpy as np

from src.base_classes.base_batch_plugin import BaseBatchPlugin

from src.enums.enums import PluginType
from src.enums.plugin_decorators import plugin_type


@plugin_type(PluginType.OSMO)
class OsmoHealthControl(BaseBatchPlugin):
    @property
    def plugin_name(self):
        return "Osmo_hc"

    lines = []

    def run_plugin(self, model):
        """Main entry point for the plugin."""
        self.set_model(model)
        self.create_composite_line_for_all_models()

    def calculate_average_line(self):
        """Calculate the average line for the given lines, normalizing them to the same number of points."""

        # Find the maximum number of points across all lines (after normalization)
        max_length = max(len(line[0]) for line in self.lines)

        # Normalize the lines by interpolating them to the same length (max_length)
        normalized_lines = []
        for line in self.lines:
            x, y = line  # O values and EI values
            normalized_x = np.linspace(x.min(), x.max(), max_length)
            normalized_y = np.interp(normalized_x, x, y)
            normalized_lines.append((normalized_x, normalized_y))

        # Calculate the average line by averaging the y-values at each x-point
        avg_y = np.mean([y for _, y in normalized_lines], axis=0)

        # Return the average line, using the normalized x-values
        return normalized_lines[0][0], avg_y

    def create_composite_line_for_all_models(self):
        """Create a composite line element with separate lines for each model, and an average line."""

        for model in self.model.models:
            self.lines.append((model.O, model.EI))

        self.add_composite_line_element(self.lines, label="Combined pO2 vs EI")

        # Calculate the average line
        avg_x, avg_y = self.calculate_average_line()

        # Add the average line
        self.add_line_element(avg_x, avg_y, label="Average pO2 vs EI")
