from abc import ABCMeta, abstractmethod
from custom_types.directions import Directions


class DirectionHavingInterface(metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def direction() -> Directions:
        pass
