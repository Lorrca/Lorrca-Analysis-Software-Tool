from src.base_classes.base_data_loader import BaseDataLoader
from src.models.osmo_model import OsmoModel
from src.utils.data_validator import DataValidator


class OsmoDataLoader(BaseDataLoader):
    """Reader for Osmo measurement files."""

    REQUIRED_DATA_KEYS = {"A", "SdA", "B", "SdB", "Eof", "O.", "EI", "SdEI"}

    def extract_metadata(self, row, meta_data) -> bool:
        """Specialized metadata extraction for osmo files."""
        if not row:
            return False

        metadata_mappings = {
            "Upper limit area": "upper_limit",
            "Lower limit area": "lower_limit",
            "Data (Y-M-D)": "date",
            "Instrument info": "instrument_info",
            "Measurement ID": "measurement_id"
        }

        for key, metadata_key in metadata_mappings.items():
            if key in row[0] and len(row) > 1:
                meta_data[metadata_key] = row[1].strip() if "limit" not in key else int(
                    row[1].strip())
                return True
        return False

    def load_data(self, filepath: str) -> OsmoModel:
        """Load data from a file and return an OsmoModel instance."""
        meta_data, data = super().load_data(filepath)

        if not DataValidator.validate_file(data, meta_data, self.REQUIRED_DATA_KEYS):
            raise ValueError(
                f"File '{filepath}' failed validation. Check its structure and content.")

        return OsmoModel(data=data, metadata=meta_data)
