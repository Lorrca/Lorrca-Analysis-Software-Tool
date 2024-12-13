import logging
from typing import Set, List, Union

from src.base_classes.base_scan_model import BaseScanModel
from src.models.osmo_model import OsmoModel
from src.models.osmo_data_loader import OsmoDataLoader
from src.models.oxy_data_loader import OxyDataLoader
from src.models.oxy_model import OxyModel
from src.utils.file_reader_helper import FileHelper

logger = logging.getLogger(__name__)


class ModelContainer:
    """Container for managing and storing models."""

    # Define a registry for the data loaders
    data_loader_registry = {
        "osmo": OsmoDataLoader(),
        "oxy": OxyDataLoader()
    }

    def __init__(self):
        self.loader = None  # This will store the current loader instance (e.g., OsmoDataLoader)
        self.single_models: Set[BaseScanModel] = set()  # Initially can hold any model type
        self.model_type = None  # Will be set after the first model is loaded

    def determine_loader(self, file_path: str):
        """Determine the appropriate loader for the file."""
        if self.loader:
            return self.loader

        try:
            headers = FileHelper.peek_headers(file_path)

            # Select the loader based on the file headers
            if "O." in headers:
                self.loader = self.data_loader_registry["osmo"]
                self.model_type = OsmoModel
                return self.loader
            elif "pO2" in headers:
                self.loader = self.data_loader_registry["oxy"]
                self.model_type = OxyModel
                return self.loader

            raise ValueError(f"No appropriate loader found for the given file: {file_path}")
        except Exception as e:
            logger.error(f"Error determining loader for file {file_path}: {e}")
            raise

    def load_files(self, file_paths: List[str]):
        """Load multiple files and add them to the container."""
        models = set()
        for file_path in file_paths:
            model = self._load_data(file_path)
            if model:
                models.add(model)
            else:
                logger.warning(f"Failed to load model from file: {file_path}")

            self.single_models.update(models)

    def _load_data(self, file_path: str) -> Union[BaseScanModel, None]:
        """Dynamically determine the loader and load the data."""
        try:
            loader = self.determine_loader(file_path)
            model = loader.load_data(file_path)

            # Ensure the model matches the expected type for the container
            if self.model_type and not isinstance(model, self.model_type):
                raise TypeError(
                    f"Loaded model type '{type(model)}' does not match expected type '{self.model_type}'")

            return model
        except Exception as e:
            logger.error(f"Error loading data from {file_path}: {e}")
            return None

    def _add_single_model(self, model):
        """Store a single model."""
        self.single_models.add(model)  # No need to use a dictionary, just add to the set
        logger.info(f"Single model added with ID: {model.id}")

    def get_single_model_by_id(self, model_id: str):
        """Retrieve a single model by its ID."""
        return next((model for model in self.single_models if model.id == model_id), None)

    def get_all_single_models(self):
        return self.single_models

    def print_all_models(self):
        """Print all models stored in the container."""
        if self.single_models:
            print("Single Models:")
            for model in self.single_models:
                print(model)
