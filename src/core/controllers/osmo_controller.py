
from src.core.models.osmo_model import OsmoModel
from src.utils.osmo_data_loader import OsmoDataLoader
from src.utils.osmo_visualization import OsmoVisualizer


class OsmoController:
    def __init__(self, data_loader: OsmoDataLoader):
        self.data_loader = data_loader
        self.model = None

    def load_data(self):
        """Load data using DataLoader and initialize the OsmoModel."""
        osmo_data, osmo_metadata = self.data_loader.load_data()
        self.model = OsmoModel(osmo_data, osmo_metadata)

    def visualize_results(self):
        """Visualize the results using OsmoVisualizer."""
        visualizer = OsmoVisualizer(self.model)
        visualizer.visualize_raw()
