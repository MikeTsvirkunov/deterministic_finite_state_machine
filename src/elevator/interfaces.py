from abc import ABCMeta, abstractmethod

from elevator.additional_types import DoorsStates


class StageHavingInterface(metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def stage(self) -> int:
        pass


class DoorsStateHavingInterface(metaclass=ABCMeta):

    @property
    @abstractmethod
    def doors_state(self) -> DoorsStates:
        pass


class IsMovedUpFlagHavingInterface(metaclass=ABCMeta):

    @property
    @abstractmethod
    def is_moved_up(self) -> bool:
        pass


class IsMovedDownFlagHavingInterface(metaclass=ABCMeta):

    @property
    @abstractmethod
    def is_moved_down(self) -> bool:
        pass


class IsDoorsOpenedOnCurrentStateFlagHavingInterface(metaclass=ABCMeta):

    @property
    @abstractmethod
    def is_doors_opened_on_current_state(self) -> bool:
        pass


class IsDoorsOpenedOnNextStateFlagHavingInterface(metaclass=ABCMeta):

    @property
    @abstractmethod
    def is_doors_opened_on_next_state(self) -> bool:
        pass


class IsMaxStageEstimateFlagHavingInterface(metaclass=ABCMeta):

    @property
    @abstractmethod
    def is_max_stage_estimate(self) -> bool:
        pass


class IsMinStageEstimateFlagHavingInterface(metaclass=ABCMeta):

    @property
    @abstractmethod
    def is_min_stage_estimated(self) -> bool:
        pass


class StageDeltaHavingInterface(metaclass=ABCMeta):

    @property
    @abstractmethod
    def stage_delta(self) -> bool:
        pass
