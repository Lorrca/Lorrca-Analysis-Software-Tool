from abc import ABC, abstractmethod


class FolderSelector(ABC):
    @abstractmethod
    def select_folder(self) -> str:
        """Open a folder selection dialog and return the selected folder path."""
        pass
