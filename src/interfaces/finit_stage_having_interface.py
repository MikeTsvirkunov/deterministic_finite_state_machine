from abc import ABCMeta, abstractmethod


class FinitStageHavingInterface(metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def finit_stage() -> int:
        pass
