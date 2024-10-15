import sys, os
from typing import Any

sys.path.append(os.path.join(sys.path[0] + '/../../'))

from src.interfaces.current_stage_having_interface import CurrentStageHavingInterface
from src.interfaces.is_door_open_interface import IsDoorOpenInterface
from src.rules.is_not_moving_with_open_doors_rule import IsNotMovingWithOpenDoorsRule
from tests.supports.getters import parse_bool

import pytest
from pytest_bdd import given, scenarios, when, then, parsers
from unittest.mock import Mock



scenarios("../features/is_not_moving_with_open_doors_rule.feature")


@given(
    "Current stage.", 
    target_fixture='current_stage',
)
def current_stage():
    return Mock(spec=int)


@given(
    "Next stage is equal to current stage.", 
    target_fixture='next_stage',
)
def next_stage(current_stage):
    return current_stage


@given(
    "Next stage is not equal to current stage.", 
    target_fixture='next_stage',
)
def next_stage():
    return Mock(spec=int)


@given(
    "Door is opened in current state.", 
    target_fixture='is_door_opened_in_current_state',
)
def is_door_opened_in_current_state():
    return True


@given(
    "Door is closed in current state.", 
    target_fixture='is_door_opened_in_current_state',
)
def is_door_opened_in_current_state():
    return False


@given(
    "Next door state is equal to current state.", 
    target_fixture='is_door_opened_in_next_state',
)
def is_door_opened_in_next_state(is_door_opened_in_current_state):
    return is_door_opened_in_current_state


@given(
    "Next door state is not equal to current state.", 
    target_fixture='is_door_opened_in_next_state',
)
def is_door_opened_in_next_state(is_door_opened_in_current_state, ):
    return not is_door_opened_in_current_state


@given(
    'Current state.',
    target_fixture='current_state',
)
def current_state(current_stage, is_door_opened_in_current_state):
    state = Mock(
        spec=IsDoorOpenInterface | CurrentStageHavingInterface, 
        current_stage=current_stage, 
        is_door_open=is_door_opened_in_current_state
    )
    return state


@given(
    'Next state.', 
    target_fixture='next_state',
)
def next_state(next_stage, is_door_opened_in_next_state):
    state = Mock(
        spec=IsDoorOpenInterface | CurrentStageHavingInterface, 
        current_stage=next_stage, 
        is_door_open=is_door_opened_in_next_state
    )
    return state


@when('Calling is not moving with open doors rule.', target_fixture='rule_result')
def rule_result(current_state, next_state):
    return IsNotMovingWithOpenDoorsRule()((current_state, next_state))


@then(
    parsers.cfparse(
        "Have been gotted {result:result} resulte.", 
        extra_types={"result": str}
    )
)
def gotted_result(result, rule_result):
    result = parse_bool(result)
    assert rule_result == result, f'Gotted {result} but expected {rule_result}'
