from src.base_classes.base_batch_plugin import BaseBatchPlugin
from src.enums.enums import PluginType
from src.enums.plugin_decorators import plugin_type


@plugin_type(PluginType.OXY)
class OsmoHealthControl(BaseBatchPlugin):
    @property
    def plugin_name(self):
        return "Oxy_hc"

    def run_plugin(self, model):
        """Main entry point for the plugin."""
        self.set_model(model)
        self.create_composite_line_for_all_models()

    def create_composite_line_for_all_models(self):
        """Create a composite line element with separate lines for each model."""
        lines = []

        for model in self.model.models:
            lines.append((model.pO2, model.EI))

        self.add_composite_line_element(lines, label="Combined pO2 vs EI")
