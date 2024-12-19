from dataclasses import dataclass

from src.base_classes.base_scan_model import BaseScanModel


@dataclass(eq=False, repr=False)
class OxyModel(BaseScanModel):
    """Data container for oxy data and metadata."""

    def __getattr__(self, item):
        # Convert attribute-like access for oxy_data keys

        if item == "name":
            return self.metadata["patient_name"]
        return super().__getattr__(item)
