import sys, os
from typing import Any

from checkers.is_current_stage_equal_to_finit_stage_checker import IsCurrentStageEquealToFinitStageChecker
from interfaces.current_stage_having_interface import CurrentStageHavingInterface
from interfaces.finit_stage_having_interface import FinitStageHavingInterface
from tests.supports.getters import parse_bool

sys.path.append(os.path.join(sys.path[0] + '/../../'))

from pytest_bdd import given, scenarios, when, then, parsers
from unittest.mock import Mock


scenarios("../features/is_current_stage_equal_to_finit_stage_checker.feature")


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
        "Task that having finit stage {position} than current elevator stage."
    ),
    target_fixture='task'
)
def task(position, elevator):
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

    task = Mock(spec=FinitStageHavingInterface)
    task.finit_stage = position
    return task


@when('Calling is_current_stage_equal_to_finit_stage_checker.', target_fixture='call_result')
def call_result(elevator, task):
    return IsCurrentStageEquealToFinitStageChecker()(elevator=elevator, task=task)


@then(
    parsers.parse(
        'Have been gotted {expected_result} resulte.'
    )
)
def check_result(expected_result, call_result):
    expected_result = parse_bool(expected_result)
    assert call_result == expected_result, 'Incorrect return value'
