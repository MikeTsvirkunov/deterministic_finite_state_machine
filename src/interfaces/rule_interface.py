from abc import ABC, abstractmethod
from typing import Any


class RuleInterface(ABC):
    @abstractmethod
    def __call__(self, data: Any) -> bool:
        pass