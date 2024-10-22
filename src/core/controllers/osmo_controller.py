from src.core.models.osmo_model import OsmoModel
from src.utils.osmo_data_loader import OsmoDataLoader
from src.utils.osmo_visualization import OsmoVisualizer


class OsmoController:
    def __init__(self, data_loader: OsmoDataLoader):
        self.data_loader = data_loader
        self.model = None
        self.results = {}
        self.osmo_metadata = None

    def load_data(self):
        """Load data using DataLoader and initialize the OsmoModel."""
        osmo_data, self.osmo_metadata = self.data_loader.load_data()
        self.model = OsmoModel(osmo_data)

    def calculate_results(self):
        """Calculate results based on the loaded model."""
        if self.model is None:
            raise ValueError("Model is not initialized. Please load data first.")

        self.results['first_peak'] = self.model.first_peak
        self.results['o_min'] = self.model.valley[0]
        self.results['ei_min'] = self.model.valley[1]
        self.results['o_max'] = self.model.o_max
        self.results['ei_max'] = self.model.ei_max
        self.results['o_hyper'] = self.model.o_hyper
        self.results['ei_hyper'] = self.model.ei_hyper
        self.results['valley'] = self.model.valley

    def visualize_results(self):
        """Visualize the results using OsmoVisualizer."""
        visualizer = OsmoVisualizer(self.results, self.model.data, self.osmo_metadata)
        visualizer.visualize_raw()