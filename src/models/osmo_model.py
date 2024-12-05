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
