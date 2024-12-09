from dataclasses import dataclass
import numpy as np


@dataclass
class OsmoModel:
    """Data container for osmo data and metadata."""
    data: dict[str, np.ndarray]
    metadata: dict

    def __getattr__(self, item):
        # Convert attribute-like access for osmo_data keys
        if item in self.data:
            return self.data[item]
        # Explicitly map non-standard keys like "O."
        if item == "O":
            return self.data["O."]
        # Check osmo_metadata as fallback
        if item in self.metadata:
            return self.metadata[item]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}'")

    def __hash__(self):
        """Hash the model using its data and metadata."""
        data_hashable = tuple((k, tuple(v)) for k, v in self.data.items())
        metadata_hashable = tuple(self.metadata.items())
        return hash((data_hashable, metadata_hashable))

    def __eq__(self, other):
        """Check equality of two OsmoModel instances."""
        if not isinstance(other, OsmoModel):
            return False

        return (self.data == other.data) and (self.metadata == other.metadata)
