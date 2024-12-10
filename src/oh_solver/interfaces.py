from abc import ABCMeta, abstractmethod
from typing import Callable


class ActionHavingInterface(metaclass=ABCMeta):

    @property
    @abstractmethod
    def action(self) -> Callable:
        pass
