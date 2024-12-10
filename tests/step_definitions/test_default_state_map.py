from typing import Callable, Collection
import ioc
from pytest_bdd import given, scenarios, when, then, parsers
from unittest.mock import Mock, patch

import sys, os
sys.path.append(os.path.join(sys.path[0] + '/../../'))

from dfsm.initiators import rules_providing, validators_providing
from src.dfsm.state_maps import DefaultStateMap
from src.dfsm.interfaces import StateInterface, BranchStateInterface


scenarios("../features/default_state_map.feature")



@given(
    'some set of not dublicated branches.',
    target_fixture='set_of_branches'
)
def get_set_of_not_dublicated_branches():
    set_of_branches = []

    b = Mock(spec=BranchStateInterface)
    b.__hash__ = lambda _: 0
    b.__eq__ = lambda s, v: s.__hash__() == v.__hash__() 
    set_of_branches.append(b)

    b = Mock(spec=BranchStateInterface)
    b.__hash__ = lambda _: 1
    b.__eq__ = lambda s, v: s.__hash__() == v.__hash__() 
    set_of_branches.append(b)

    b = Mock(spec=BranchStateInterface)
    b.__hash__ = lambda _: 2
    b.__eq__ = lambda s, v: s.__hash__() == v.__hash__() 
    set_of_branches.append(b)

    return set_of_branches


@given(
    'some alpha states branch in this set.',
    target_fixture='alpha_state_in_set'
)
def alpha_state(set_of_branches):
    b = Mock(spec=BranchStateInterface)
    b.name = Mock(name='alpha_state')
    b.from_state = Mock(StateInterface)
    b.to_state = Mock(StateInterface)
    b.__hash__ = lambda _: 1000
    b.__eq__ = lambda s, v: s.__hash__() == v.__hash__() 
    set_of_branches.append(b)
    return b, set_of_branches


@given(
    'default state map.',
    target_fixture='default_state_map'
)
def alpha_state(alpha_state_in_set):
    rules_providing()
    validators_providing()
    return alpha_state_in_set, DefaultStateMap(source_states_map=alpha_state_in_set[1])


@given(
    'some set of branches with dublicates.',
    target_fixture='set_of_branches'
)
def get_set_of_branches_with_dublicates():
    set_of_branches = []

    b = Mock(spec=BranchStateInterface)
    b.__hash__ = lambda _: 0
    b.__eq__ = lambda s, v: s.__hash__() == v.__hash__() 
    set_of_branches.append(b)

    b = Mock(spec=BranchStateInterface)
    b.__hash__ = lambda _: 1
    b.__eq__ = lambda s, v: s.__hash__() == v.__hash__() 
    set_of_branches.append(b)

    b = Mock(spec=BranchStateInterface)
    b.__hash__ = lambda _: 1
    b.__eq__ = lambda s, v: s.__hash__() == v.__hash__() 
    set_of_branches.append(b)

    return set_of_branches

@when(
    'try create default state map.',
    target_fixture='result'
)
def try_create_default_state_map(set_of_branches):
    rules_providing()
    validators_providing()
    try:
        return DefaultStateMap(source_states_map=set_of_branches)
    except Exception as e:
        return e


@when(
    'try get next state for alpha state.',
    target_fixture='result'
)
def try_get_next_state_for_alpha_state(default_state_map):
    (a, ssm), sm = default_state_map
    r = sm.next(branch_name=a.name, state=a.from_state)
    return a, r


@then(
    'have been gotted error.',
)
def gotted_this_another_alpha_state(result):
    
    assert isinstance(result, Exception), 'Not gotted exception.'
    t = AttributeError('Setting state_map with dublicates.').args
    assert result.args == t


@then(
    'default state map successfully created.',
)
def gotted_this_another_alpha_state(result):
    assert type(result) == DefaultStateMap, f'Gotted {type(result)} not DefaultStateMap'


@then(
    'have been gotted next state for alpha state.',
)
def gotted_this_another_alpha_state(
    result: StateInterface
):
    a, r = result
    assert r == a.to_state, f'Gotted {r} not {a.to_state}'
