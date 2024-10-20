import ioc
from interfaces.current_stage_having_interface import CurrentStageHavingInterface
from interfaces.direction_having_interface import DirectionHavingInterface
from interfaces.rule_interface import RuleInterface
from interfaces.start_stage_having_interface import StartStageHavingInterface
from states.requests_tasks_queues_transfer_state import RequestsTasksQueuesTransferState


def requestsTasksQueuesTransferStateBuilder(
    elevator: DirectionHavingInterface | CurrentStageHavingInterface, 
    request: DirectionHavingInterface | StartStageHavingInterface
) -> RequestsTasksQueuesTransferState:
    is_request_queue_empty_checker: RuleInterface = ioc.require('Variables.Checkers.IsRequestQueueEmptyChecker')
    is_current_stage_equal_to_start_stage_checker: RuleInterface = ioc.require('Variables.Checkers.IsCurrentStageEquealToStartStageChecker')
    is_moving_by_direction_checker: RuleInterface = ioc.require('Variables.Checkers.IsMovingByDirectionChecker')
    state = RequestsTasksQueuesTransferState(
        is_request_queue_empty=is_request_queue_empty_checker(),
        is_directions_equal=is_moving_by_direction_checker(elevator=elevator, task=request),
        is_stage_equals=is_current_stage_equal_to_start_stage_checker(elevator=elevator, request=request)
    )
    return state