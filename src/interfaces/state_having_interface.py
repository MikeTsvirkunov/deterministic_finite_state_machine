from abc import ABCMeta, abstractmethod


class StateHavingInterface(metaclass=ABCMeta):
    @abstractmethod
    @property
    def state(self) -> int:
        pass