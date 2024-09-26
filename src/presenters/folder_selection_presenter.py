from src.core.usecases.folder_selection_usecase import FolderSelectionUseCase


class FolderSelectionPresenter:
    def __init__(self, view, folder_selection_use_case: FolderSelectionUseCase):
        self.view = view
        self.folder_selection_use_case = folder_selection_use_case

    def on_select_data_folder(self):
        """Handle folder selection for data folder."""
        self._select_folder("data", self.view.set_data_folder)

    def on_select_hc_data_folder(self):
        """Handle folder selection for HCData folder."""
        self._select_folder("HCdata", self.view.set_hc_data_folder)

    def on_select_results_folder(self):
        """Handle folder selection for results folder."""
        self._select_folder("results", self.view.set_results_folder)

    def _select_folder(self, folder_type: str, update_method):
        """Generic method to select a folder and update the UI."""
        try:
            folder = self.folder_selection_use_case.select_single_folder(folder_type)
            update_method(folder)
        except ValueError as e:
            self.view.display_error(str(e))
