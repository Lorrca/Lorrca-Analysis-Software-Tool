from src.base_classes.base_data_loader import BaseDataLoader
from src.models.oxy_model import OxyModel
from src.utils.data_validator import DataValidator


class OxyDataLoader(BaseDataLoader):
    """Reader for Oxy measurement files."""

    REQUIRED_DATA_KEYS = {"A", "B", "EI", "pO2", "N2"}

    def extract_metadata(self, row, meta_data) -> bool:
        """Specialized metadata extraction for oxy files."""
        if not row:
            return False

        metadata_mappings = {
            "Upper limit area": "upper_limit",
            "Lower limit area": "lower_limit",
            "Data (Y-M-D)": "date",
            "Patient name": "patient_name"
        }

        for key, metadata_key in metadata_mappings.items():
            if key in row[0] and len(row) > 1:
                meta_data[metadata_key] = row[1].strip() if "limit" not in key else int(
                    row[1].strip())
                return True
        return False

    def load_data(self, filepath: str) -> OxyModel:
        """Load data from a file and return an OxyModel instance."""
        meta_data, data = super().load_data(filepath)

        if not DataValidator.validate_file(data, meta_data, self.REQUIRED_DATA_KEYS):
            raise ValueError(
                f"File '{filepath}' failed validation. Check its structure and content.")

        return OxyModel(data=data, metadata=meta_data)
