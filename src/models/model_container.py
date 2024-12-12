import logging
import uuid
from dataclasses import dataclass, field
from typing import Dict, Set, List, Union

from src.models.osmo_model import OsmoModel
from src.models.osmo_data_loader import load_data

logger = logging.getLogger(__name__)


@dataclass
class ModelContainer:
    """Container for managing and storing models."""
    single_models: Dict[str, OsmoModel] = field(default_factory=dict)  # Individual models by ID
    model_sets: Dict[str, Set[OsmoModel]] = field(
        default_factory=dict)  # Sets of models by batch ID

    def load_file(self, file_path: str):
        """Load a single file and add it to the container."""
        model = self._load_data(file_path)
        if model:
            self._add_single_model(model)
        else:
            logger.warning(f"Failed to load model from file: {file_path}")

    def load_files(self, file_paths: List[str], batch: bool = False):
        """Load multiple files and add them to the container."""
        models = set()
        for file_path in file_paths:
            model = self._load_data(file_path)
            if model:
                models.add(model)
            else:
                logger.warning(f"Failed to load model from file: {file_path}")

        if batch:
            self._add_batch_model_set(models)
        else:
            for model in models:
                self._add_single_model(model)

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
        model_id = str(uuid.uuid4())
        self.single_models[model_id] = model
        logger.info(f"Single model added with ID: {model_id}")

    def _add_batch_model_set(self, model_set: Set[OsmoModel]):
        """Store a set of models."""
        if model_set:
            batch_id = str(uuid.uuid4())
            self.model_sets[batch_id] = model_set
            logger.info(f"Batch model set added with Batch ID: {batch_id}")
        else:
            logger.warning("Attempted to add an empty model set.")

    def print_all_models(self):
        """Print all models stored in the container."""
        print("Single Models:")
        for model_id, model in self.single_models.items():
            print(
                f"ID: {model_id}, Measurement ID: {model.metadata.get('measurement_id', 'No Measurement ID')}")

        # Only print model sets if they exist
        if self.model_sets:
            print("\nModel Sets:")
            for batch_id, model_set in self.model_sets.items():
                print(
                    f"Batch ID: {batch_id}, Models: {[m.metadata.get('measurement_id', 'No Measurement ID') for m in model_set]}")
