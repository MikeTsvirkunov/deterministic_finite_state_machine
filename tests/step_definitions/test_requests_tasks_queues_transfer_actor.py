import sys, os
from typing import Any, Callable, Iterable

import ioc

from actors.requests_tasks_queues_transfer_actor import RequestsTasksQueuesTransferActor
from builders.requests_tasks_queues_transfer_state_builder import requestsTasksQueuesTransferStateBuilder
from checkers.is_current_stage_equal_to_start_stage_checker import IsCurrentStageEquealToStartStageChecker
from checkers.is_request_queue_empty_checker import IsRequestQueueEmptyChecker
from constants.requests_tasks_queues_transfer_state_mapper import REQUESTS_TASKS_QUEUES_TRANSFER_STATE_MAPPER
from custom_types.directions import Directions
from interfaces.current_stage_having_interface import CurrentStageHavingInterface
from interfaces.start_stage_having_interface import StartStageHavingInterface
from interfaces.task_queue_having_interface import TaskQueueHavingInterface
from states.requests_tasks_queues_transfer_state import RequestsTasksQueuesTransferState

sys.path.append(os.path.join(sys.path[0] + '/../../'))

from checkers.is_moving_by_direction_checker import IsMovingByDirectionChecker
from interfaces.direction_having_interface import DirectionHavingInterface
from tests.supports.getters import parse_bool, parse_direction

import pytest
from pytest_bdd import given, scenarios, when, then, parsers
from unittest.mock import Mock

from interfaces.rule_interface import RuleInterface


scenarios("../features/requests_tasks_queues_transfer_actor.feature")


@given(
    parsers.parse(
        "Elevator with current stage and current direction."
    ),
    target_fixture='current_elevator'
)
def current_elevator():
    elevator = Mock(spec=DirectionHavingInterface | CurrentStageHavingInterface | TaskQueueHavingInterface)
    elevator.direction = Mock(spec=str)
    elevator.current_stage = Mock(spec=int)
    elevator.current_stage = Mock(spec=int)
    elevator.task_queue = Mock(spec=list)
    elevator.task_queue.__len__ = lambda s: 0
    def on_append(e):
        elevator.task_queue.__len__ = lambda s: 1
    elevator.task_queue.append = Mock(spec=Callable, return_value=None, side_effect=on_append)
    return elevator


@given(
    parsers.parse(
        "Request with {direction_state} direction and {stage_state} start stage."
    ),
    target_fixture='current_request'
)
def current_request(direction_state, stage_state, current_elevator):
    request = Mock(spec=StartStageHavingInterface | DirectionHavingInterface)

    request.start_stage = Mock(int)
    if stage_state == 'same':
        request.start_stage.__eq__ = lambda a, b: True
        current_elevator.current_stage.__eq__ = lambda a, b: True
    elif stage_state == 'different':
        request.start_stage.__eq__ = lambda a, b: False
        current_elevator.current_stage.__eq__ = lambda a, b: False
    
    request.direction = Mock(spec=str)
    if direction_state == 'same':
        request.direction.__eq__ = lambda a, b: True
        current_elevator.direction.__eq__ = lambda a, b: True
    elif direction_state == 'different':
        request.direction.__eq__ = lambda a, b: False
        current_elevator.direction.__eq__ = lambda a, b: False
    return request


@given(
    parsers.parse(
        "Not empty requests queue with current request."
    )
)
def current_request_queue(current_request):
    request_queue = Mock(spec=list)
    request_queue.__len__ = Mock(spec=Callable, return_value=1)
    request_queue.pop = Mock(spec=Callable, return_value=current_request)
    def on_pop(idx):
        request_queue.__len__ = Mock(spec=Callable, return_value=0)
        return current_request
    request_queue.pop = Mock(spec=Callable, return_value=current_request, side_effect=on_pop)
    request_queue.__getitem__ = Mock(spec=Callable, return_value=current_request)
    ioc.provide('Variables.RequestsQueue', request_queue)


@given(
    parsers.parse(
        "Empty requests queue."
    )
)
def current_request_queue():
    request_queue = Mock(spec=list)
    request_queue.__len__ = Mock(spec=Callable, return_value=0)
    def on_pop(idx):
        raise Exception('Empty requests queue.')
    request_queue.pop = Mock(spec=Callable, side_effect=on_pop)
    ioc.provide('Variables.RequestsQueue', request_queue)


@when('When calling requests tasks queues transfer actor.')
def call_result(current_elevator):
    actor = RequestsTasksQueuesTransferActor()
    ioc.provide('Variables.Checkers.IsMovingByDirectionChecker', IsMovingByDirectionChecker())
    ioc.provide('Variables.Checkers.IsCurrentStageEquealToStartStageChecker', IsCurrentStageEquealToStartStageChecker())
    ioc.provide('Variables.Checkers.IsRequestQueueEmptyChecker', IsRequestQueueEmptyChecker())
    ioc.provide('Bulders.RequestsTasksQueuesTransferStateBuilder', requestsTasksQueuesTransferStateBuilder)
    ioc.provide('Bulders.RequestsTasksQueuesTransferStateMapper', REQUESTS_TASKS_QUEUES_TRANSFER_STATE_MAPPER)
    actor(elevator=current_elevator)


@then(
    parsers.parse(
        'Request has been added to elevator task queue.'
    )
)
def check_result(current_elevator, current_request):
    current_elevator: TaskQueueHavingInterface = current_elevator
    p: Mock = current_elevator.task_queue.append
    p.assert_called_with(current_request)


@then(
    parsers.parse(
        'Elevator task queue was not changed.'
    )
)
def check_result(current_elevator):
    current_elevator: TaskQueueHavingInterface = current_elevator
    p: Mock = current_elevator.task_queue.append
    p.assert_not_called()


@then(
    parsers.parse(
        'Request has been deleted from request queue.'
    ), 
    target_fixture='check_result'
)
def check_result():
    request_queue: Mock = ioc.require('Variables.RequestsQueue')
    request_queue.pop.assert_called_once()
    assert len(request_queue) == 0, 'Value was not deleted.'


@then(
    parsers.parse(
        'Request has not been deleted from request queue.'
    ), 
    target_fixture='check_result'
)
def check_result():
    request_queue: Mock = ioc.require('Variables.RequestsQueue')
    request_queue.pop.assert_not_called()
    assert len(request_queue) != 0, 'Value was deleted.'
