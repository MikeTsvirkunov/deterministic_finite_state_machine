from abc import ABC, abstractmethod
from typing import Any


class RuleInterface(ABC):
    @abstractmethod
    def __call__(self, *args, **kwds) -> bool:
        pass