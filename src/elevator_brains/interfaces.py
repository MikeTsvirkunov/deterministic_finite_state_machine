from abc import ABCMeta, abstractmethod
from typing import Collection

from elevator.additional_types import Direction


class FromStageHavingInterface(metaclass=ABCMeta):

    @property
    @abstractmethod
    def from_stage(self) -> int:
        pass


class ToStageHavingInterface(metaclass=ABCMeta):

    @property
    @abstractmethod
    def to_stage(self) -> int:
        pass


class TaskQueueHavingInterface(metaclass=ABCMeta):

    @property
    @abstractmethod
    def task_queue(self) -> Collection[ToStageHavingInterface]:
        pass


class DirectionHavingInterface(metaclass=ABCMeta):

    @property
    @abstractmethod
    def direction(self) -> Direction:
        pass


class RequestQueueHavingInterface(metaclass=ABCMeta):

    @property
    @abstractmethod
    def request_queue(self) -> Collection[FromStageHavingInterface | ]:
        pass
