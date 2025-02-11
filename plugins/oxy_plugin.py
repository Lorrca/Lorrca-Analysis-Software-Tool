import numpy as np

from src.base_classes.base_plugin import BasePlugin
from src.enums.enums import PluginType
from src.enums.plugin_decorators import plugin_type

@plugin_type(PluginType.OXY)
class OxyPlugin(BasePlugin):
    @property
    def plugin_name(self):
        return "OxyPlugin"

    def run_plugin(self, model):
        """Main entry point for the plugin."""
        self.set_model(model)
        self.raw_po2_vs_ei()
        self.calculate_sum_a_b()
        self.raw_t_vs_ei()
        self.raw_t_vs_po2()

    def raw_po2_vs_ei(self):
        po2 = self.model.pO2
        ei = self.model.EI
        self.add_line_element(po2, ei, label=f"pO2 vs EI({self.model.name})")

    def calculate_sum_a_b(self):
        """Fetch A and B, compute their sum, and visualize it."""
        a = self.model.A  # Fetch A
        b = self.model.B  # Fetch B
        t = self.model.t  # Fetch time

        sum_ab = a + b  # Compute A + B

        self.add_line_element(t, sum_ab, label=f"(A + B)({self.model.name})")  # Set y-axis limits

    def raw_t_vs_ei(self):
        t = self.model.t
        ei = self.model.EI
        self.add_line_element(t, ei, label=f"EI({self.model.name})")  # Set y-axis limits

    def raw_t_vs_po2(self):
        po2 = self.model.pO2
        t = self.model.t

        # Find the index of the minimum PO2 value
        min_index = np.argmin(po2)
        min_t = t[min_index]  # Corresponding T value
        min_po2 = po2[min_index]  # Minimum PO2 value

        # Add a red dot at the min(pO2) point
        self.add_line_element([min_t], [min_po2], label=f"Min pO2: {min_po2:.2f}", color="red", marker="o", linestyle="None")