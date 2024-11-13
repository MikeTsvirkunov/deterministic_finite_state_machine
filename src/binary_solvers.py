from abc import ABCMeta, abstractmethod
from typing import Callable, Dict


class BinarySolverInterface(metaclass=ABCMeta):

    @property
    @abstractmethod
    def binary_actions_map(self) -> Dict[bool, Callable]:
        pass


    @abstractmethod
    def __call__(self, boolean: bool) -> Callable:
        pass


class DefaultBinarySolver(BinarySolverInterface):

    def __init__(self, binary_actions_map: Dict[bool, Callable]) -> None:
        self.__binary_actions_map__: Dict[bool, Callable] = binary_actions_map
    

    @property
    def binary_actions_map(self) -> Dict[bool, Callable]:
        raise AttributeError('Not availablre value.')
    

    def __call__(self, boolean) -> Callable:
        return self.__binary_actions_map__[boolean]
