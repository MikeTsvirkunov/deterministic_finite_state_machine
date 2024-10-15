from abc import ABCMeta, abstractmethod


class IsDoorOpenInterface(ABCMeta):
    
    @property
    @abstractmethod
    def is_door_open() -> bool:
        pass
