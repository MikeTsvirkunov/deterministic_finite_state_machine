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
from elevator.branch_rule import BranchIsUniqueForStatesMap, IsClosingDoorsCorrect, IsMovingDownCorrect, IsMovingFromAvailableStage, IsMovingToAvailableStage, IsMovingUpCorrect, IsOpeningDoorsCorrect, MultyRule
from elevator.interfaces import DoorsStateHavingInterface, IsDoorsOpenedOnCurrentStateFlagHavingInterface, IsDoorsOpenedOnNextStateFlagHavingInterface, IsMaxStageEstimateFlagHavingInterface, IsMinStageEstimateFlagHavingInterface, IsMovedDownFlagHavingInterface, IsMovedUpFlagHavingInterface, StageDeltaHavingInterface, StageHavingInterface
from elevator.state_map_builder import DefaultStateMapGenerator
from elevator_brains.interfaces import ElevatorCommandHavingInterface
from oh_solver.interfaces import ActionHavingInterface
from oh_solver.oh_solver import OHSolver

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

    rules_providing()
    validators_providing()
    ioc.provide('Constants.Building.MaxStage', max_stage)
    ioc.provide('Constants.Building.MinStage', min_stage)
    def build_rull_state(cmd, is_current_doors_opened, is_next_doors_opened, is_moved_up, is_moved_down, is_min_stage_estimated, is_max_stage_estimated, stage_delta):
        r = Mock(
            spec=IsMovedUpFlagHavingInterface | 
                IsMovedDownFlagHavingInterface | 
                IsDoorsOpenedOnCurrentStateFlagHavingInterface | 
                IsDoorsOpenedOnNextStateFlagHavingInterface | 
                ElevatorCommandHavingInterface |
                IsMinStageEstimateFlagHavingInterface |
                IsMaxStageEstimateFlagHavingInterface |
                StateInterface |
                StageDeltaHavingInterface
        )
        r.elevator_command = cmd
        r.is_moved_down = is_moved_down
        r.is_moved_up = is_moved_up
        r.is_doors_opened_on_next_state = is_next_doors_opened
        r.is_doors_opened_on_current_state = is_current_doors_opened
        r.is_min_stage_estimated = is_min_stage_estimated
        r.is_max_stage_estimated = is_max_stage_estimated
        r.stage_delta = stage_delta
        r.__eq__ = lambda s, v: (
            v.elevator_command == s.elevator_command and 
            v.is_moved_down == s.is_moved_down and 
            v.is_moved_up == s.is_moved_up and 
            v.is_doors_opened_on_next_state == s.is_doors_opened_on_next_state and 
            v.is_doors_opened_on_current_state == s.is_doors_opened_on_current_state and 
            s.is_max_stage_estimated == v.is_max_stage_estimated and 
            s.is_min_stage_estimated == v.is_min_stage_estimated and
            s.stage_delta == v.stage_delta
        )
        r.__hash__ = lambda s: f'{s.elevator_command} {s.is_moved_up} {s.is_moved_down} {s.is_doors_current_on_current_state} {s.is_doors_next_on_current_state} {s.stage_delta}'.__hash__()
        return r
    

    def build_from_elevator_state(elevator_branch: BranchStateInterface):
        max_stage = ioc.require('Constants.Building.MaxStage')
        min_stage = ioc.require('Constants.Building.MinStage')
        from_state: StageHavingInterface | DoorsStateHavingInterface | StateInterface = elevator_branch.from_state
        to_state: StageHavingInterface | DoorsStateHavingInterface | StateInterface = elevator_branch.to_state
        is_moved_down = from_state.stage > to_state.stage
        is_moved_up = from_state.stage < to_state.stage
        stage_delta = abs(from_state.stage - to_state.stage)
        is_current_doors_opened = from_state.doors_state == DoorsStates.opened
        is_next_doors_opened = to_state.doors_state == DoorsStates.opened 
        cmd: ElevatorCommands = elevator_branch.name
        is_min_stage_estimated = min_stage == from_state.stage
        is_max_stage_estimated = max_stage == from_state.stage
        return build_rull_state(cmd, is_current_doors_opened, is_next_doors_opened, is_moved_up, is_moved_down, is_min_stage_estimated, is_max_stage_estimated, stage_delta)
    
    ioc.provide('Actions.BuildRullState', build_from_elevator_state)
    ea = Mock(spec=ActionHavingInterface | StateInterface)
    ea.__hash__ = lambda _: 'ea'.__hash__()
    ea.__eq__ = lambda s, v: s.__hash__() == v.__hash__()
    ea.action = empty_action
    ioc.provide('Constants.States.EmptyAction', ea)

    addact = Mock(spec=ActionHavingInterface | StateInterface)
    addact.__hash__ = lambda _: 'addact'.__hash__()
    addact.__eq__ = lambda s, v: s.__hash__() == v.__hash__()
    addact.action = insert_value_to_list
    list_of_rules_processed = list()
    for ri in list_of_rules.split('\n')[1:]:
        cmd, is_current_doors_opened, is_next_doors_opened, is_moved_up, is_moved_down, is_min_stage_estimated, is_max_stage_estimated, stage_delta = ri[1:-1].replace(' ', '').split('|')
        ri_s = build_rull_state(
            ElevatorCommands(cmd.replace('_', ' ')), 
            is_current_doors_opened=='1', 
            is_next_doors_opened=='1', 
            is_moved_up=='1', 
            is_moved_down=='1', 
            is_min_stage_estimated=='1', 
            is_max_stage_estimated=='1', 
            int(stage_delta)
        )
        bi = Mock(BranchStateInterface)
        bi.from_state = ri_s
        bi.to_state = addact
        bi.name = None
        list_of_rules_processed.append(bi)
    return OHSolver(list_of_rules_processed)


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
    ioc.provide('Rules.BranchRuleStateMap', list_of_rules)
    ioc.provide('Builders.ElevatorState.Builder.Default', mock_state_builder)
    ioc.provide('Builders.ElevatorBranchState.Builder.Default', mock_branch_builder)
    ioc.provide('Builders.StatesMap.Default', mock_states_map_builder)


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
# Ветки лампорта
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
