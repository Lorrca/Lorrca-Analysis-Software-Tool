from src.core.interfaces.folder_selector import FolderSelector


class FolderSelectionUseCase:
    def __init__(self, folder_selector: FolderSelector):
        self.folder_selector = folder_selector

    def select_single_folder(self, folder_type: str) -> str:
        """Select a single folder and return its path."""
        folder_path = self.folder_selector.select_folder()
        if not folder_path:
            raise ValueError(f"No folder selected for {folder_type}")
        return folder_path
