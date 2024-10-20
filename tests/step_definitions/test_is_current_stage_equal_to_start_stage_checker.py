import sys, os
from typing import Any

from checkers.is_current_stage_equal_to_start_stage_checker import IsCurrentStageEquealToStartStageChecker
from interfaces.current_stage_having_interface import CurrentStageHavingInterface
from interfaces.finit_stage_having_interface import FinitStageHavingInterface
from tests.supports.getters import parse_bool

sys.path.append(os.path.join(sys.path[0] + '/../../'))

from pytest_bdd import given, scenarios, when, then, parsers
from unittest.mock import Mock


scenarios("../features/is_current_stage_equal_to_start_stage_checker.feature")


@given(
    "Elevator with current stage.",
    target_fixture='elevator'
)
def elevator():
    elevator = Mock(spec=CurrentStageHavingInterface)
    elevator.current_stage = Mock(spec=int)
    return elevator


@given(
    parsers.parse(
        "Request that having start stage {position} than current elevator stage."
    ),
    target_fixture='current_request'
)
def current_request(position, elevator):
    if position == 'lower':
        position = Mock(spec=int)
        position.__eq__ = lambda s, b: False
        elevator.current_stage.__eq__ = lambda s, b: False
    
    elif position == 'higher':
        position: int = Mock(spec=int)
        position.__eq__ = lambda s, b: False
        elevator.current_stage.__eq__ = lambda s, b: False
    

    elif position == 'equal':
        position: int = Mock(spec=int)
        position.__eq__ = lambda s, b: True
        elevator.current_stage.__eq__ = lambda s, b: True

    request = Mock(spec=FinitStageHavingInterface)
    request.start_stage = position
    return request


@when('Calling is_current_stage_equal_to_start_stage_checker.', target_fixture='call_result')
def call_result(elevator, current_request):
    return IsCurrentStageEquealToStartStageChecker()(elevator=elevator, request=current_request)


@then(
    parsers.parse(
        'Have been gotted {expected_result} resulte.'
    )
)
def check_result(expected_result, call_result):
    expected_result = parse_bool(expected_result)
    assert call_result == expected_result, 'Incorrect return value'
