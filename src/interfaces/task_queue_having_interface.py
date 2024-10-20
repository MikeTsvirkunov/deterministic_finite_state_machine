from abc import ABCMeta, abstractmethod
from typing import Iterable


class TaskQueueHavingInterface(metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def task_queue() -> Iterable:
        pass
