from abc import abstractmethod, ABC

from interfaces.state_interface import StateInterface

class StateContainerInterface(ABC):
    @abstractmethod
    def __call__(self, state: StateInterface) -> StateInterface:
        pass

# шпрингер Зверев Иван