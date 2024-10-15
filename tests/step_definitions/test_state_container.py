import sys, os
sys.path.append(os.path.join(sys.path[0] + '/../../'))

import pytest
from pytest_bdd import given, scenarios, when, then
from unittest.mock import Mock

from src.interfaces.state_interface import StateInterface
from src.states.state_container import StateContainer
from tests.supports.getters import get_table


scenarios("../features/state_container.feature")  


@pytest.fixture  
def state_1():
    state_1 = Mock(spec=StateInterface, )
    hash_for_state_1 = Mock(spec=int)
    hash_for_state_1.return_value = int(1)
    state_1.__hash__ = hash_for_state_1
    return state_1


@pytest.fixture  
def state_2():
    state_2 = Mock(spec=StateInterface, )
    hash_for_state_2 = Mock(spec=int)
    hash_for_state_2.return_value = int(2)
    state_2.__hash__ = hash_for_state_2
    return state_2


@pytest.fixture  
def state_3():
    state_3 = Mock(spec=StateInterface, )
    hash_for_state_3 = Mock(spec=int)
    hash_for_state_3.return_value = int(3)
    state_3.__hash__ = hash_for_state_3
    return state_3


@given("State container that match state_1 with state_2, and state_1 have didn't match to state_3.", target_fixture='state_container')
def state_container(state_1, state_2):
    container={state_1: state_2}
    return StateContainer(container=container)



@when("Getting match state to state_1.", target_fixture='gotted_state')
def gotted_state(state_container, state_1):
    return state_container(state_1)


@then("Have been gotted state_2.")
def get_num_of_stages(gotted_state, state_2, state_3):
    assert gotted_state == state_2, f"Gotted state is {gotted_state} and not equal to state_2 that is {state_2}"
    assert gotted_state != state_3, f"Gotted state is {gotted_state} and equal to state_3 that is {state_3}"

    