from abc import ABCMeta, abstractmethod


class TaskQueueHavingInterface(metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def task_queue() -> int:
        pass
