from typing import Collection, List
import ioc
from actions import empty_action
from binary_solvers import DefaultBinarySolver
from elevator.interfaces import StageHavingInterface
from elevator_brains.additional_types import Directions
from elevator_brains.interfaces import DirectionHavingInterface, FromStageHavingInterface, TaskQueueHavingInterface


def add_request_to_elevator(elevator: TaskQueueHavingInterface | StageHavingInterface | DirectionHavingInterface) -> None:
    requests_queue: List[FromStageHavingInterface | DirectionHavingInterface] = ioc.require('Globals.RequestsQueue')
    a = list(filter(lambda a: a.direction != elevator.direction or elevator.stage != a.from_stage, requests_queue))
    elevator.task_queue += list(filter(lambda a: a.direction == elevator.direction and elevator.stage == a.from_stage, requests_queue))
    requests_queue.clear()
    requests_queue.extend(a)


def remove_request_to_elevator(elevator: TaskQueueHavingInterface | StageHavingInterface | DirectionHavingInterface) -> None:
    elevator.task_queue = list(filter(lambda a: elevator.stage != a.to_stage, elevator.task_queue))


def update_direction_max(elevator: DirectionHavingInterface):
    a = Directions.down
    elevator.direction = a


def update_direction_min(elevator: DirectionHavingInterface):
    a = Directions.up
    elevator.direction = a



ELEVATOR_REQUEST_QUEUE_INSERT_SOLVER = DefaultBinarySolver(
    {
        True: add_request_to_elevator,
        False: empty_action
    }
)


ELEVATOR_TASK_QUEUE_CLEAN_SOLVER = DefaultBinarySolver(
    {
        True: remove_request_to_elevator,
        False: empty_action
    }
)

ELEVATOR_DIRECTION_MAX_ESTIMATE_UPDATER_SOLVER = DefaultBinarySolver(
    {
        True: update_direction_max,
        False: empty_action
    }
)


ELEVATOR_DIRECTION_MIN_ESTIMATE_UPDATER_SOLVER = DefaultBinarySolver(
    {
        True: update_direction_min,
        False: empty_action
    }
)
