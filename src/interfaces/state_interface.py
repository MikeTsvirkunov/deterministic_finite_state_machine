from abc import abstractmethod, ABCMeta

class StateInterface(ABCMeta):

    @abstractmethod
    def __hash__(self) -> int:
        pass

# шпрингер Зверев Иван