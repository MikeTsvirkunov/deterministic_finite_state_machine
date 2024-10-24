from abc import ABCMeta, abstractmethod


class StartStageHavingInterface(metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def start_stage() -> int:
        pass
