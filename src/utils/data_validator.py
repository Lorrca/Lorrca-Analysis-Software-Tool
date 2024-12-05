import numpy as np


class DataValidator:
    @staticmethod
    def validate_file(data: dict[str, np.ndarray], metadata: dict, data_keys: set[str]) -> bool:
        required_data_keys = data_keys
        if not isinstance(data, dict) or not isinstance(metadata, dict):
            print("Validation Error: Data and metadata must be dictionaries.")
            return False

        # Check for required keys
        missing_keys = required_data_keys - data.keys()
        if missing_keys:
            print(f"Validation Error: Missing required keys in data: {missing_keys}")
            return False

        return True
