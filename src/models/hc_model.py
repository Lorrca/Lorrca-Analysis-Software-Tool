import uuid
from dataclasses import field, dataclass
from typing import List

from src.base_classes.base_scan_model import BaseScanModel


@dataclass
class HCModel:
    """Model for Healthy Control data."""
    name: str
    models: List[BaseScanModel] = field(default_factory=list)
    models_selection: dict[str, bool] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def is_empty(self) -> bool:
        return not bool(self.models)

    def add_model(self, model: BaseScanModel):
        if model not in self.models:
            self.models.append(model)
            self.models_selection[model.id] = True
        else:
            print(f"Model {model} already exists in HC_Model")

    def remove_model(self, model: BaseScanModel):
        if model in self.models:
            self.models.remove(model)
            self.models_selection.pop(model.id, None)

    def change_model_selection(self, model_id, is_selected):
        """Change the selection state of a model."""
        if model_id in self.models_selection:
            self.models_selection[model_id] = is_selected
        else:
            print(f"Model with ID {model_id} does not exist in selection.")

    def __hash__(self):
        """Hash based on the unique ID."""
        return hash(self.id)

    def __eq__(self, other):
        """Equality based on unique ID."""
        if not isinstance(other, HCModel):
            return False
        return self.id == other.id

    def __repr__(self):
        return f"HC_Model(name={self.name}, id={self.id}, models_count={len(self.models)})"
