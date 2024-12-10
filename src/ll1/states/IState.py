from abc import ABCMeta, abstractmethod

class IState(metaclass=ABCMeta):
    @abstractmethod
    def transition(self):
        pass