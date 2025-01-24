from src.base_classes.base_hc_plugin import BaseHCPlugin


class HealthControl(BaseHCPlugin):
    @property
    def plugin_name(self):
        return "Healthy Control"

    @property
    def is_healthy_control(self) -> bool:
        return True

    def run_plugin(self, model):
        """Main entry point for the plugin."""
        self.set_model(model)
        self.create_composite_line_for_all_models()

    def create_composite_line_for_all_models(self):
        """Create a composite line element with separate lines for each model."""
        lines = []

        for model in self.model.base_models:
            lines.append((model.O, model.EI))

        self.add_composite_line_element(lines, label="Combined pO2 vs EI")
