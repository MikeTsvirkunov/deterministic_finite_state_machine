from abc import ABCMeta, abstractmethod


class RequestQueueHavingInterface(metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def request_queue() -> int:
        pass
