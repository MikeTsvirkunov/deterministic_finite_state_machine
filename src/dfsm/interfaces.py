from abc import ABCMeta, abstractmethod
from typing import Any, Collection, Iterable


class StateInterface(metaclass=ABCMeta):
    
    def __hash__(self) -> str:
        pass


    def __eq__(self, value) -> bool:
        pass


class BranchStateInterface(metaclass=ABCMeta):

    @property
    @abstractmethod
    def name(self):
        pass


    @property
    @abstractmethod
    def from_state(self) -> StateInterface:
        pass


    @property
    @abstractmethod
    def to_state(self) -> StateInterface:
        pass


class StateMapInterface(metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def states_map(self) -> Collection[BranchStateInterface]:
        pass


    @abstractmethod
    def next(self, branch_name: Any, state: StateInterface) -> StateInterface:
        pass


class RuleInterface(metaclass=ABCMeta):
    
    @abstractmethod
    def __call__(self, *args, **kwargs) -> bool:
        pass


class CorrectHavingInterface(metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def is_correct(self) -> bool:
        pass


class ExtendableInterface(metaclass=ABCMeta):
    
    @abstractmethod
    def extend(self, value: Any) -> None:
        pass


class ValidatorInterface(metaclass=ABCMeta):
    
    @abstractmethod
    def validate(self, *args, **kwargs) -> Any:
        pass


class StateHavingInterface(metaclass=ABCMeta):

    @property
    @abstractmethod
    def state(self) -> StateInterface:
        pass

