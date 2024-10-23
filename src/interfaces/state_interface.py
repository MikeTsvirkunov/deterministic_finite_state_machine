from abc import abstractmethod, ABCMeta

class StateInterface(metaclass=ABCMeta):

    @abstractmethod
    def __hash__(self) -> int:
        pass

    
    @abstractmethod
    def __eq__(self, other) -> int:
        pass

# шпрингер Зверев Иван
