from dataclasses import dataclass, field
import numpy as np
import uuid


@dataclass
class BaseScanModel:
    """Data container for measurement data and metadata."""
    data: dict[str, np.ndarray]
    metadata: dict
    id: str = field(default_factory=lambda: str(uuid.uuid4()))  # Automatically assign an ID

    def __getattr__(self, item):
        # Convert attribute-like access for data keys
        if item in self.data:
            return self.data[item]
        # Check metadata as fallback
        if item in self.metadata:
            return self.metadata[item]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}'")

    def __hash__(self):
        """Hash the model using its data and metadata."""
        data_hashable = tuple((k, tuple(v)) for k, v in self.data.items())
        metadata_hashable = tuple(self.metadata.items())
        return hash((data_hashable, metadata_hashable))

    def __eq__(self, other):
        """Check equality of two BaseModel instances."""
        if isinstance(other, BaseScanModel):
            return False

        # Compare data dictionaries, using numpy's array_equal to compare arrays
        if self.data.keys() != other.data.keys():
            return False

        # Check whether any of the arrays are not equal.
        if any(not np.array_equal(value, other.data[key]) for key, value in self.data.items()):
            return False

        # Compare metadata dictionaries
        if self.metadata != other.metadata:
            return False

        return True

    def __repr__(self):
        """Base representation for Model printing."""
        return f"{self.__class__.__name__}(id={self.id})"
