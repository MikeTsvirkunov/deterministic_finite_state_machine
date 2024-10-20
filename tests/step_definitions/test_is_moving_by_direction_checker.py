import sys, os
from typing import Any

sys.path.append(os.path.join(sys.path[0] + '/../../'))

from checkers.is_moving_by_direction_checker import IsMovingByDirectionChecker
from interfaces.direction_having_interface import DirectionHavingInterface
from tests.supports.getters import parse_bool, parse_direction

import pytest
from pytest_bdd import given, scenarios, when, then, parsers
from unittest.mock import Mock

from interfaces.rule_interface import RuleInterface


scenarios("../features/is_moving_by_direction_checker.feature")


@given(
    parsers.parse(
        "Elevator with {elevator_direction} direction."
    ),
    target_fixture='elevator'
)
def elevator(elevator_direction):
    elevator = Mock(spec=DirectionHavingInterface)
    elevator.direction = parse_direction(elevator_direction)
    return elevator


@given(
    parsers.parse(
        "Request that is {task_direction} request on qurrent stage."
    ),
    target_fixture='task'
)
def task(task_direction):
    task = Mock(spec=DirectionHavingInterface)
    task.direction = parse_direction(task_direction)
    return task


@when('Calling is_moving_by_direction_checker.', target_fixture='call_result')
def call_result(elevator, task):
    return IsMovingByDirectionChecker()(elevator=elevator, task=task)


@then(
    parsers.parse(
        'Have been gotted {expected_result} resulte.'
    ), 
    target_fixture='check_result'
)
def check_result(expected_result, call_result):
    expected_result = parse_bool(expected_result)
    assert call_result == expected_result, 'Incorrect return value'
