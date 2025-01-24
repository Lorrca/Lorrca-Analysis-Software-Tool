from src.base_classes.base_plugin import BasePlugin


class OxyPlugin(BasePlugin):
    @property
    def plugin_name(self):
        return "OxyPlugin"

    def run_plugin(self, model):
        """Main entry point for the plugin."""
        self.set_model(model)
        self.raw_po2_vs_ei()

    def raw_po2_vs_ei(self):
        po2 = self.model.pO2
        ei = self.model.EI

        self.add_line_element(po2, ei, label="pO2 vs EI")
