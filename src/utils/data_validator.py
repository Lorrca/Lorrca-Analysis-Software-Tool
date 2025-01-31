import logging

import numpy as np

logger = logging.getLogger(__name__)


class DataValidator:
    @staticmethod
    def validate_file(data: dict[str, np.ndarray], metadata: dict, data_keys: set[str]) -> bool:
        required_data_keys = data_keys
        if not isinstance(data, dict) or not isinstance(metadata, dict):
            logger.error("Validation Error: Data and metadata must be dictionaries.")
            return False

        # Check for required keys
        missing_keys = required_data_keys - data.keys()
        if missing_keys:
            logger.error(f"Validation Error: Missing required keys in data: {missing_keys}")
            return False

        return True
