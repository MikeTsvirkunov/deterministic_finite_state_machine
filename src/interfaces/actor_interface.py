from abc import ABC, abstractmethod
from typing import Any


class ActorInterface(ABC):
    @abstractmethod
    def __call__(self, *args, **kwds) -> None:
        pass