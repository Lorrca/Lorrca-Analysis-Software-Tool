from dataclasses import dataclass, field
from typing import Dict, Set, List, Union
import uuid

from src.models.osmo_model import OsmoModel


@dataclass
class ModelContainer:
    """Generic container for storing model instances."""
    single_models: Dict[str, OsmoModel] = field(
        default_factory=dict)  # Store individual models by ID
    model_sets: Dict[str, Set[OsmoModel]] = field(default_factory=dict)  # Store sets by batch ID

    def add_model(self, model: Union[OsmoModel, List[OsmoModel], Set[OsmoModel]]):
        """Add a model, a list of models, or a set of models to the container."""
        if isinstance(model, list):
            # List of models, assign unique IDs to each and store
            for m in model:
                model_id = str(uuid.uuid4())
                self.single_models[model_id] = m
        elif isinstance(model, set):
            # Batch upload (set of models), assign a single ID to the set
            batch_id = str(uuid.uuid4())
            self.model_sets[batch_id] = model
        else:
            # Single model, assign unique ID and store
            model_id = str(uuid.uuid4())
            self.single_models[model_id] = model

    def get_single_model(self, model_id: str) -> Union[OsmoModel, None]:
        """Retrieve a single model by its unique ID."""
        return self.single_models.get(model_id, None)

    def get_model_set(self, batch_id: str) -> Union[Set[OsmoModel], None]:
        """Retrieve a set of models by its batch ID."""
        return self.model_sets.get(batch_id, None)

    def print_all_models(self):
        """Print all the models stored in the container."""
        print("Single Models:")
        for model_id, model in self.single_models.items():
            print(f"ID: {model_id}")

        print("\nModel Sets:")
        for batch_id, model_set in self.model_sets.items():
            print(f"Batch ID: {batch_id}")
