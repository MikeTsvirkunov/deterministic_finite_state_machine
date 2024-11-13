from pytest_bdd import given, scenarios, when, then, parsers
from unittest.mock import Mock

import sys, os

from dfsm.rules import StateMapContainNoDublicates
sys.path.append(os.path.join(sys.path[0] + '/../../'))

from src.dfsm.interfaces import BranchStateInterface


scenarios("../features/state_map_contain_no_dublicates_rule.feature")



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
    'calling this rule.',
    target_fixture='result'
)
def try_create_default_state_map(set_of_branches):
    r = StateMapContainNoDublicates()
    return r(states_map=set_of_branches)


@then(
    parsers.cfparse(
        'gotted {expected_result:value}.',
        extra_types={"value": str}
    )
)
def gotted_result(expected_result: str, result: bool):
    er = expected_result == 'True'
    assert result == er
