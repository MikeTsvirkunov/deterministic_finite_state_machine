from abc import ABCMeta, abstractmethod


class StartStageHavingInterface(meta=ABCMeta):
    
    @property
    @abstractmethod
    def start_stage() -> int:
        pass
