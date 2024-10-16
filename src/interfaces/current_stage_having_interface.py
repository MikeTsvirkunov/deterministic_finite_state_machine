from abc import ABCMeta, abstractmethod


class CurrentStageHavingInterface(metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def current_stage() -> int:
        pass
