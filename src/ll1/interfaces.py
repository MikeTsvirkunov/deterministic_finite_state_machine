from abc import abstractmethod, ABCMeta
from typing import Collection


class CurrentStateIdHavingInterface(metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def from_state_id(self) -> int:
        pass


class NextStateIdHavingInterface(metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def next_state_id(self) -> int:
        pass


class FollowingSymbolsHavingInterface(metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def next_state_id(self) -> int:
        pass


class ApplyStrategyHavingInterface(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def __call__(current_idx: int, next_idx: int) -> int:
        pass


class ApplyStrategyHavingInterface(metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def apply(self) -> ApplyStrategyHavingInterface:
        pass
