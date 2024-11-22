from src.interfaces.plugin_interface import PluginInterface


class ExamplePlugin(PluginInterface):
    def __init__(self, model, plot_manager):
        super().__init__(model, plot_manager)

    def run_plugin(self):
        """Implement the plugin's main functionality."""
        self._raw_curve()
        self._max_value()
        self._area()

    def get_plugin_name(self) -> str:
        """Return the name of this plugin."""
        return "Example Plugin"

    def _raw_curve(self):
        raw_o_range = self.model.get_o
        raw_ei_range = self.model.get_ei
        self.plot_manager.add_line(
            raw_o_range,
            raw_ei_range,
            label="Raw O vs EI",
            plugin_name=self.get_plugin_name()
        )

    def _max_value(self):
        o_max = self.model.get_o_max
        ei_max = self.model.get_ei_max
        self.plot_manager.add_point(
            o_max,
            ei_max,
            label="Max Value",
            plugin_name=self.get_plugin_name()
        )

    def _area(self):
        _, segment_o, segment_ei = self.model.get_area
        self.plot_manager.add_area(
            segment_o,
            segment_ei,
            label="Segment Area",
            plugin_name=self.get_plugin_name()
        )
