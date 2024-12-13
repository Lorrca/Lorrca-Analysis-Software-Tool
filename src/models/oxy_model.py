from dataclasses import dataclass

from src.base_classes.base_scan_model import BaseScanModel


@dataclass(eq=False, repr=False)
class OxyModel(BaseScanModel):
    """Data container for oxy data and metadata."""
