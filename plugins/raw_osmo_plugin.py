from src.base_classes.base_plugin import BasePlugin


class ExamplePlugin(BasePlugin):
    @property
    def plugin_name(self):
        return "Example Plugin"

    def run_plugin(self):
        """Implement the plugin's main functionality."""
        self._raw_curve()
        self._max_value()
        self._area()

    def _raw_curve(self):
        raw_o_range = self.model.get_o
        raw_ei_range = self.model.get_ei

        self.add_line_element(
            raw_o_range,
            raw_ei_range,
            label="Raw O vs EI"
        )

    def _max_value(self):
        o_max = self.model.get_o_max
        ei_max = self.model.get_ei_max

        self.add_point_element(
            o_max,
            ei_max,
            label="Max Value"
        )

    def _area(self):
        area, o_segment, ei_segment = self.model.get_area

        self.add_area_element(
            x=o_segment,
            y1=ei_segment,
            y2=[0] * len(ei_segment),  # Baseline of 0 for the area
            label=f"Segment Area (Area={area:.2f})"
        )
