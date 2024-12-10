from abc import ABCMeta, abstractmethod


class DoorsStateHavingInterface(metaclass=ABCMeta):
    @abstractmethod
    @property
    def doors_state(self) -> int:
        pass