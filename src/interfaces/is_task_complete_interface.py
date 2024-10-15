from abc import ABCMeta, abstractmethod


class IsTaskCompleteInterface(ABCMeta):
    
    @property
    @abstractmethod
    def is_task_complete() -> bool:
        pass
