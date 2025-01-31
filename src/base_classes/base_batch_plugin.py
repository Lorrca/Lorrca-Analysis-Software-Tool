from abc import abstractmethod, ABC

from src.base_classes.base_plugin import BasePlugin, UnionList
from src.models.batch_model import BatchModel


class BaseBatchPlugin(BasePlugin, ABC):
    @abstractmethod
    def run_plugin(self, model: BatchModel):
        pass

    def add_line_element(self, x: UnionList, y: UnionList, label: str,
                         is_reference=False, **kwargs):
        super().add_line_element(x, y, label, is_batch=True, is_reference=is_reference, **kwargs)

    def add_point_element(self, x: float, y: float, label: str,
                          is_reference=False, **kwargs):
        super().add_point_element(x, y, label, is_batch=True, is_reference=is_reference, **kwargs)

    def add_area_element(self, x: UnionList, y1: UnionList, y2: UnionList, label: str,
                         is_reference=False, **kwargs):
        super().add_area_element(x, y1, y2, label, is_batch=True, is_reference=is_reference,
                                 **kwargs)

    def add_composite_line_element(self, lines: list[tuple], label: str,
                                   is_reference=False, **kwargs):
        super().add_composite_line_element(lines, label, is_batch=True, is_reference=is_reference,
                                           **kwargs)
