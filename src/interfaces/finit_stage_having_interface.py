from abc import ABCMeta, abstractmethod


class FinitStageHavingInterface(meta=ABCMeta):
    
    @property
    @abstractmethod
    def finit_stage() -> int:
        pass
