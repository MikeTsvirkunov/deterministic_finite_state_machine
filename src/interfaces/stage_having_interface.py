from abc import ABCMeta, abstractmethod
from typing import Any


class StageHavingInterface(ABCMeta):
    
    @property
    @abstractmethod
    def stage() -> int:
        pass
