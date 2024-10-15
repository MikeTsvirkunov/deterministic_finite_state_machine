from abc import ABCMeta, abstractmethod


class StartStageHavingInterface(ABCMeta):
    
    @property
    @abstractmethod
    def start_stage() -> int:
        pass
