import uuid
from dataclasses import field, dataclass
from typing import List

from src.base_classes.base_scan_model import BaseScanModel


@dataclass
class HCModel:
    """Model for Healthy Control data."""
    name: str
    base_models: List[BaseScanModel] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def add_model(self, model: BaseScanModel):
        if model not in self.base_models:
            self.base_models.append(model)
        else:
            print(f"Model {model} already exists in HC_Model")

    def remove_model(self, model: BaseScanModel):
        if model in self.base_models:
            self.base_models.remove(model)

    def __hash__(self):
        """Hash based on the unique ID."""
        return hash(self.id)

    def __eq__(self, other):
        """Equality based on unique ID."""
        if not isinstance(other, HCModel):
            return False
        return self.id == other.id

    def __repr__(self):
        return f"HC_Model(name={self.name}, id={self.id}, models_count={len(self.base_models)})"
