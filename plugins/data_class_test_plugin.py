import numpy as np

from src.base_classes.base_plugin import BasePlugin


class RawCurve(BasePlugin):
    @property
    def plugin_name(self):
        return "Dataclass Raw Plugin"

    def run_plugin(self, model):
        """Main entry point for the plugin."""
        self.model = model
        self.raw_o_vs_ei_curve()
        self.highest_point()

    def raw_o_vs_ei_curve(self):
        """Plot O vs EI raw curve."""
        o_data = self.model.O
        ei_data = self.model.EI

        self.add_line_element(o_data, ei_data, label="O vs Ei RAW")

    def highest_point(self):
        """Find and mark the highest EI value on the curve."""
        ei_data = self.model.EI
        o_data = self.model.O

        ei_max, max_idx = self.calculate_max_with_index(ei_data)
        corresponding_o = o_data[max_idx]

        # Mark the point on the plot
        self.add_point_element(corresponding_o, ei_max, label="Highest EI Point")

    @staticmethod
    def calculate_max_with_index(values: np.ndarray) -> tuple[float, int]:
        """Calculate the maximum value and its index."""
        if values.size == 0:
            raise ValueError("Data array is empty. Cannot calculate maximum.")
        max_value = float(np.max(values))
        max_index = int(np.argmax(values))
        return max_value, max_index
