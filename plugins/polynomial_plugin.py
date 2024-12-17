from numpy import polyfit, polyval, linspace
from src.base_classes.base_plugin import BasePlugin


class PolynomialPlugin(BasePlugin):
    @property
    def plugin_name(self):
        return "Polynomial Plugin"

    def run_plugin(self, model):
        """Implement the plugin's main functionality."""
        self.model = model

        self._polynomial_curve()

    def _polynomial_curve(self):
        """Generate and plot a polynomial curve based on the model's data."""
        raw_o_range = self.model.O
        raw_ei_range = self.model.EI

        # Fit a polynomial to the data (degree 3, as an example)
        degree = 8
        coefficients = polyfit(raw_o_range, raw_ei_range, degree)

        # Generate a smooth curve using the polynomial
        smooth_o = linspace(min(raw_o_range), max(raw_o_range), 500)
        smooth_ei = polyval(coefficients, smooth_o)

        self.add_line_element(smooth_o, smooth_ei, label="Polynomial O vs EI")
