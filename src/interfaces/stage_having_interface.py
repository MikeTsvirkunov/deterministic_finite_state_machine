from abc import ABCMeta, abstractmethod
from typing import Any


class StageHavingInterface(meta=ABCMeta):
    
    @property
    @abstractmethod
    def stage() -> int:
        pass
