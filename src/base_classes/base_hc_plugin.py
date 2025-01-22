from abc import abstractmethod, ABC

from src.base_classes.base_plugin import BasePlugin
from src.models.hc_model import HCModel


class BaseHCPlugin(BasePlugin, ABC):
    @abstractmethod
    def run_plugin(self, model: HCModel):
        """Method to be implemented by subclasses for plugin-specific logic."""
        pass
