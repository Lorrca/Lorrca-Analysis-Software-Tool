import logging
from dataclasses import dataclass, field
from typing import Set, List, Union, Dict

from src.models.osmo_model import OsmoModel
from src.models.osmo_data_loader import load_data

logger = logging.getLogger(__name__)


@dataclass
class ModelContainer:
    """Container for managing and storing models."""
    single_models: Set[OsmoModel] = field(
        default_factory=set)  # Store models directly (no need for ids)
    model_sets: Dict[str, Set[OsmoModel]] = field(
        default_factory=dict)  # Sets of models by batch ID

    def load_file(self, file_path: str):
        """Load a single file and add it to the container."""
        model = self._load_data(file_path)
        if model:
            self._add_single_model(model)
        else:
            logger.warning(f"Failed to load model from file: {file_path}")

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

    @staticmethod
    def _load_data(file_path: str) -> Union[OsmoModel, None]:
        """Simulated method to load model data from a file path."""
        try:
            return load_data(file_path)
        except Exception as e:
            logger.error(f"Error loading data from {file_path}: {e}")
            return None

    def _add_single_model(self, model: OsmoModel):
        """Store a single model."""
        self.single_models.add(model)  # No need to use a dictionary, just add to the set
        logger.info(f"Single model added with ID: {model.id}")

    def get_single_model_by_id(self, model_id: str) -> Union[OsmoModel, None]:
        """Retrieve a single model by its ID."""
        return next((model for model in self.single_models if model.id == model_id), None)

    def get_all_single_models(self):
        return self.single_models

    def print_all_models(self):
        """Print all models stored in the container."""
        print("Single Models:")
        for model in self.single_models:
            print(
                f"ID: {model.id}, Measurement ID: {model.metadata.get('measurement_id', 'No Measurement ID')}")

        # Only print model sets if they exist
        if self.model_sets:
            print("\nModel Sets:")
            for batch_id, model_set in self.model_sets.items():
                print(
                    f"Batch ID: {batch_id}, Models: {[m.metadata.get('measurement_id', 'No Measurement ID') for m in model_set]}")
