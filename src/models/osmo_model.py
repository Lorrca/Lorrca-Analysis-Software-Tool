from dataclasses import dataclass

from src.base_classes.base_scan_model import BaseScanModel


@dataclass(eq=False)
class OsmoModel(BaseScanModel):
    """Data container for Osmo data and metadata."""

    def __getattr__(self, item):
        # Convert attribute-like access for osmo_data keys

        if item == "O":
            return self.data["O."]
        return super().__getattr__(item)

    def __repr__(self):
        return f"OsmoModel: ID = {self.id}, Measurement ID = {self.measurement_id}"