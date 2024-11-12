from abc import ABCMeta, abstractmethod

from elevator.additional_types import DoorsStates


class StageHavingInterface(metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def stage(self) -> int:
        pass


class DoorsStateHavingInterface(metaclass=ABCMeta):

    @property
    @abstractmethod
    def doors_state(self) -> DoorsStates:
        pass