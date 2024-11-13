from typing import Callable, Collection
import ioc
from unittest.mock import Mock
from pytest_bdd import given, scenarios, when, then, parsers
import sys, os

from actions import empty_action, insert_value_to_list
from binary_solvers import DefaultBinarySolver
from dfsm.initiators import rules_providing, validators_providing
from dfsm.interfaces import BranchStateInterface, StateInterface, StateMapInterface
from dfsm.state_maps import DefaultStateMap
from elevator.additional_types import DoorsStates, ElevatorCommands
from elevator.branch_rule import BranchIsUniqueForStatesMap, IsClosingDoorsCorrect, IsDoorsClosed, IsMovingDownCorrect, IsMovingFromAvailableStage, IsMovingOnOnlyOneStage, IsMovingToAvailableStage, IsMovingUpCorrect, IsMovingWithClosedDoors, IsOpeningDoorsCorrect, MultyRule
from elevator.interfaces import DoorsStateHavingInterface, StageHavingInterface
from elevator.state_map_builder import DefaultStateMapGenerator

sys.path.append(os.path.join(sys.path[0] + '/../../'))


scenarios("../features/states_map_generator.feature")


@given(
    parsers.cfparse(
        'that max stage is {max_stage:value}.',
        extra_types={"value": int}
    ),
    target_fixture='max_stage'
)
def get_max_stage(max_stage: int):
    return max_stage


@given(
    parsers.cfparse(
        'that min stage is {min_stage:value}.',
        extra_types={"value": int}
    ),
    target_fixture='min_stage'
)
def get_min_stage(min_stage: int):
    return min_stage


@given(
    parsers.cfparse(
        'list of rules:\n{list_of_rules:value}',
        extra_types={"value": str}
    ),
    target_fixture='list_of_rules'
)
def get_list_of_rules(list_of_rules: str, min_stage: int, max_stage: int):

    ioc.provide('Constants.Building.MaxStage', max_stage)
    ioc.provide('Constants.Building.MinStage', min_stage)

    rules_names_interpritator = {
        'IsMovingOnOnlyOneStage': IsMovingOnOnlyOneStage(),
        'IsMovingWithClosedDoors': IsMovingWithClosedDoors(),
        'IsDoorsClosed': IsDoorsClosed(),
        'IsMovingToAvailableStage': IsMovingToAvailableStage(),
        'IsMovingFromAvailableStage': IsMovingFromAvailableStage(),
        'BranchIsUniqueForStatesMap': BranchIsUniqueForStatesMap(),
        'IsClosingDoorsCorrect': IsClosingDoorsCorrect(),
        'IsMovingUpCorrect': IsMovingUpCorrect(),
        'IsMovingDownCorrect': IsMovingDownCorrect(),
        'IsOpeningDoorsCorrect': IsOpeningDoorsCorrect(),
    }
    list_of_rules_processed = [rules_names_interpritator[rule_i] for rule_i in list_of_rules.split('\n')]
    return list_of_rules_processed


@when(
    'building states map by this rules.',
    target_fixture='generated_states_map'
)
def build_state_map(list_of_rules, max_stage, min_stage):
    
    def mocked_state_builder_call(stage, doors_state):
        state = Mock(spec=StateInterface | StageHavingInterface | DoorsStateHavingInterface)
        state.__hash__ = lambda _: f'Given elevator sate on {stage} with doors state {doors_state}'
        state.__eq__ = lambda s, value: value.stage == s.stage and value.doors_state == s.doors_state
        state.stage = stage
        state.doors_state = doors_state
        return state


    def mocked_branch_state_builder_call(branch_name, from_state, to_state):
        branch = Mock(spec=BranchStateInterface)
        branch.name = branch_name
        branch.from_state = from_state
        branch.to_state = to_state
        return branch
    

    def mock_states_map_builder_call(states_map):
        return DefaultStateMap(
            source_states_map=states_map
        )


    # mock_state_builder = Mock(spec=Callable[[int, DoorsStates], StateInterface])
    # mock_state_builder.__call__ = mocked_state_builder_call

    # mock_branch_builder = Mock(spec=Callable[[ElevatorCommands, StateInterface, StateInterface], BranchStateInterface])
    # mock_branch_builder.__call__ = mocked_branch_state_builder_call

    # mock_states_map_builder = Mock(spec=Callable[[Collection[BranchStateInterface]], StateMapInterface])
    # mock_states_map_builder.__call__ = mock_states_map_builder_call


    mock_state_builder = mocked_state_builder_call
    mock_branch_builder = mocked_branch_state_builder_call
    mock_states_map_builder = mock_states_map_builder_call

    ioc.provide('Values.Get.Collection', lambda : list())
    ioc.provide('Rules.BranchRule', MultyRule(rules=list_of_rules, aggregation_function=all))
    ioc.provide('Builders.ElevatorState.Builder.Default', mock_state_builder)
    ioc.provide('Builders.ElevatorBranchState.Builder.Default', mock_branch_builder)
    ioc.provide('Builders.StatesMap.Default', mock_states_map_builder)

    rules_providing()
    validators_providing()

    ioc.provide('Validators.InsertCorrectBranch', DefaultBinarySolver(
        binary_actions_map={
            True: insert_value_to_list,
            False: empty_action
        }
    ))
    g = DefaultStateMapGenerator()
    states_map = g(max_stage=max_stage, min_stage=min_stage)
    return states_map

# алгоритм рафт
# векторное время
# Лексли Лампорт

@then(
    parsers.cfparse(
        'been gotted states map:\n{expected_map:value}',
        extra_types={"value": str}
    )
)
def check_results(expected_map, generated_states_map: DefaultStateMap):
    k = 0
    e = 0
    expected_map = expected_map.split('\n')[1:]
    for row_i in expected_map:
        cmd, stage_1, doors_state_1, stage_2, doors_state_2 = row_i.replace(' ', '')[1:-1].split('|')
        stage_1 = int(stage_1)
        stage_2 = int(stage_2)
        cmd = ElevatorCommands[cmd]
        doors_state_1 = doors_state_1 == 'opened'
        doors_state_2 = doors_state_2 == 'opened'
        e += 1
        for branch_i in  generated_states_map.__states_map__:
            v0 = cmd == branch_i.name
            v1 = branch_i.from_state.stage == stage_1
            v2 = branch_i.to_state.stage == stage_2
            v3 = doors_state_1 == branch_i.from_state.doors_state.value
            v4 = doors_state_2 == branch_i.to_state.doors_state.value
            if all([v0, v2, v3, v4]):
                k += 1
    assert k == e, 'Count of equeal branches is incorrect.'
    assert len(expected_map) == len(generated_states_map.__states_map__), 'Gotted incorrect size of states map.'
