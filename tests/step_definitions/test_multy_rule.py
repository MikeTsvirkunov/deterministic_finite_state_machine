import sys, os
from typing import Any

from rules.multy_rule import MultyRule
from tests.supports.getters import parse_bool
sys.path.append(os.path.join(sys.path[0] + '/../../'))

import pytest
from pytest_bdd import given, scenarios, when, then, parsers
from unittest.mock import Mock

from interfaces.rule_interface import RuleInterface


scenarios("../features/multy_rule.feature")  


def mock_call_rule(data, result: bool):
    data()
    return result


def mock_call_rule_return_true(data):
    return mock_call_rule(data, True)


def mock_call_rule_return_false(data):
    return mock_call_rule(data, False)


@pytest.fixture  
def num_of_rules():
    return 10


@given("Data for multy rule.", target_fixture='data_for_multy_rule')
def data_for_multy_rule():
    return Mock(spec=RuleInterface)


@given(
    parsers.cfparse(
        "List of only const {data:value} rules for multy rule.", 
        extra_types={"value": str}
    ),
    target_fixture='list_of_rules_for_multy_rule'
)
def list_of_rules_for_multy_rule(num_of_rules, data):
    data: bool = parse_bool(data)
    return [Mock(spec=RuleInterface, side_effect=lambda a: mock_call_rule(a, data)) for _ in range(num_of_rules)]


@given("List of mix bool const rules for multy rule.", target_fixture='list_of_rules_for_multy_rule')
def list_of_rules_for_multy_rule(num_of_rules):
    const_true_rules = [Mock(spec=RuleInterface, return_value=True, side_effect=lambda a: mock_call_rule_return_true(a)) for _ in range(num_of_rules // 2)]
    const_false_rules = [Mock(spec=RuleInterface, return_value=True, side_effect=lambda a: mock_call_rule_return_false(a)) for _ in range(num_of_rules // 2)]
    return const_true_rules + const_false_rules


@given("Multy rule with setted list of rules.", target_fixture='multy_rule')
def multy_rule(list_of_rules_for_multy_rule):
    return MultyRule(list_of_rules=list_of_rules_for_multy_rule)


@when("Calling multy rule.", target_fixture='multy_rule_call_result')
def multy_rule_call_result(multy_rule, data_for_multy_rule):
    return multy_rule(data=data_for_multy_rule)


@then(
    parsers.cfparse(
        "Have been gotted {expected_result:value} resulte.", 
        extra_types={"value": str}
    )
)
def get_num_of_stages(expected_result, multy_rule_call_result):
    expected_result = parse_bool(expected_result)
    assert multy_rule_call_result == expected_result, f"Gotted true multy rule resulte"


@then("All rules been called.")
def get_num_of_stages(list_of_rules_for_multy_rule, data_for_multy_rule):
    for f_i in list_of_rules_for_multy_rule:
        f_i.assert_called_with(data_for_multy_rule)


# @then("All rules been called.")
# def get_num_of_stages(data_for_multy_rule: Mock):
#     data_for_multy_rule.
