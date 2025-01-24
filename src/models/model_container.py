import logging
import os
from typing import Set, List, Union, Optional

from src.base_classes.base_scan_model import BaseScanModel
from src.enums.enums import ContainerType
from src.models.hc_model import HCModel
from src.models.osmo_data_loader import OsmoDataLoader
from src.models.oxy_data_loader import OxyDataLoader
from src.utils.file_reader_helper import FileHelper

logger = logging.getLogger(__name__)

HC_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../HC')


class ModelContainer:
    """Container for managing and storing models."""

    def __init__(self):
        self.loader: Optional[Union[OsmoDataLoader, OxyDataLoader]] = None  # Current loader
        self.single_models: Set[BaseScanModel] = set()  # Set of loaded models
        self.selection_state: dict[str, bool] = {}  # Track selection state by model ID
        self.hc_models: Set[HCModel] = set()  # Set of Healthy Control Models
        self.model_type = None  # Model type (either OsmoModel or OxyModel)

    def determine_loader(self, file_path: str) -> Union[
        OsmoDataLoader, OxyDataLoader]:
        """Determine and return the appropriate loader based on the file content."""
        try:
            # Extract headers
            headers = FileHelper.peek_headers(file_path)
            # Determine the appropriate loader based on headers
            if "O." in headers:
                self.loader = OsmoDataLoader()
                self.model_type = ContainerType.OSMO
            elif "pO2" in headers:
                self.loader = OxyDataLoader()
                self.model_type = ContainerType.OXY
            else:
                raise ValueError(f"Unsupported file format for {file_path}")

            return self.loader

        except Exception as e:
            logger.error(f"Error determining loader for file {file_path}: {e}")
            raise

    def load_files(self, file_paths: List[str]):
        """Load multiple files and add them to the container."""
        models = set()
        for file_path in file_paths:
            model = self._load_data(file_path)
            if model:
                models.add(model)
            else:
                logger.warning(f"Failed to load model from file: {file_path}")

        self.single_models.update(models)
        if not self.hc_models:
            self._load_hc()

    def _load_hc(self):
        """Load all healthy control models from subfolders within the HC folder."""
        if not os.path.isdir(HC_FOLDER):
            logger.error(f"HC folder is not a directory: {HC_FOLDER}")
            return

        # Iterate over subfolders in the HC folder
        for folder_name in os.listdir(HC_FOLDER):
            folder_path = os.path.join(HC_FOLDER, folder_name)

            if not os.path.isdir(folder_path):
                logger.warning(f"Skipped non-directory item in HC folder: {folder_path}")
                continue

            self._process_folder(folder_name, folder_path)

    def _process_folder(self, folder_name, folder_path):
        """Process the folder if it contains valid model data."""
        first_file_path = self._get_first_csv_file(folder_path)
        if not first_file_path:
            logger.warning(f"No valid CSV files found in folder: {folder_path}")
            return

        first_model = self._load_data(first_file_path)
        if not first_model:
            logger.warning(
                f"First file in folder {folder_path} is not a valid model. Skipping folder.")
            return

        hc_model = HCModel(name=folder_name)

        self._process_files_in_folder(folder_path, hc_model)

        # Add the HCModel to the main collection
        self.hc_models.add(hc_model)

    def _process_files_in_folder(self, folder_path, hc_model):
        """Process all CSV files in the folder and add valid models to the HCModel."""
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path) and file_path.endswith(".CSV"):
                model = self._load_data(file_path)
                if model:
                    hc_model.add_model(model)
                else:
                    logger.warning(f"Failed to load model from file: {file_path}")

    @staticmethod
    def _get_first_csv_file(folder_path):
        """Get the first valid CSV file in the folder."""
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path) and file_path.endswith(".CSV"):
                return file_path
        return None

    def _load_data(self, file_path: str) -> Optional[BaseScanModel]:
        """Load a model based on the file using the determined loader and delimiter."""
        try:
            if self.loader is None:
                self.loader = self.determine_loader(file_path)
            model = self.loader.load_data(file_path)

            return model

        except Exception as e:
            logger.error(f"Error loading data from {file_path}: {e}")
            return None

    def get_model_by_id(self, model_id: str) -> Optional[BaseScanModel]:
        """Retrieve a model by its ID."""
        return next((model for model in self.single_models if model.id == model_id), None)

    def update_selection(self, model_id: str, selected: bool):
        """Update the selection state for a given model."""
        if model_id not in self.selection_state or self.selection_state[model_id] != selected:
            self.selection_state[model_id] = selected
            logger.info(f"Updated selection for model {model_id}: {selected}")

    def get_selected_models(self) -> List[BaseScanModel]:
        """Return a list of selected models based on the selection state."""
        selected_models = [
            model for model, selected in self.get_models_with_selection()
            if selected
        ]
        return selected_models

    def get_hc_models_with_selection(self) -> List[tuple]:
        """Return a list of HC models and their selection state."""
        return self._get_filtered_models_with_selection(HCModel)

    def get_models_with_selection(self) -> List[tuple]:
        """Return a list of all models and their selection state."""
        return self._get_filtered_models_with_selection(BaseScanModel)

    def _get_filtered_models_with_selection(self, model_filter) -> List[tuple]:
        """Filter models by type and include their selection state."""
        return [
            (model, self.selection_state.get(model.id, False))
            for model in self.single_models
            if isinstance(model, model_filter)
        ]

    def print_all_models(self):
        """Print all models stored in the container."""
        if self.single_models:
            logger.info("Models in the container:")
            for model in self.single_models:
                logger.info(model)
        else:
            logger.info("No models available in the container.")
