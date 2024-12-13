from dataclasses import dataclass


@dataclass(eq=False, repr=False)
class OxyModel:
    """Data container for oxy data and metadata."""
