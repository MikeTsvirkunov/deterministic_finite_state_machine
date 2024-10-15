from abc import ABCMeta, abstractmethod


class FinitStageHavingInterface(ABCMeta):
    
    @property
    @abstractmethod
    def finit_stage() -> int:
        pass
