from elevator.interfaces import DoorsStateHavingInterface, StageHavingInterface
from elevator_brains.constants import ELEVATOR_DIRECTION_MAX_ESTIMATE_UPDATER_SOLVER, ELEVATOR_DIRECTION_MIN_ESTIMATE_UPDATER_SOLVER, ELEVATOR_REQUEST_QUEUE_INSERT_SOLVER, ELEVATOR_TASK_QUEUE_CLEAN_SOLVER


def update_elevator_state(elevator: StageHavingInterface | DoorsStateHavingInterface, next_elevator_state: StageHavingInterface | DoorsStateHavingInterface, is_required_stage: bool, is_finit_stage: bool, is_min_stage_achived: bool, is_max_stage_achived: bool, is_empty: bool):
    a1 = ELEVATOR_REQUEST_QUEUE_INSERT_SOLVER(is_required_stage)
    a1(elevator=elevator)
    a2 = ELEVATOR_TASK_QUEUE_CLEAN_SOLVER(is_finit_stage)
    a2(elevator=elevator)
    a3 = ELEVATOR_DIRECTION_MAX_ESTIMATE_UPDATER_SOLVER(is_max_stage_achived and is_empty)
    a3(elevator=elevator)
    a4 = ELEVATOR_DIRECTION_MIN_ESTIMATE_UPDATER_SOLVER(is_min_stage_achived and is_empty)
    a4(elevator=elevator)
    elevator.doors_state = next_elevator_state.doors_state
    elevator.stage = next_elevator_state.stage

