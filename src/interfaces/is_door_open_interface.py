from abc import ABCMeta, abstractmethod


class IsDoorOpenInterface(metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def is_door_open() -> bool:
        pass
