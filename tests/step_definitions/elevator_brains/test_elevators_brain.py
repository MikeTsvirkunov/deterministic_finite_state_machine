import json
from typing import Callable, Collection
import ioc
from unittest.mock import Mock
from pytest_bdd import given, scenarios, when, then, parsers
import sys, os

sys.path.append(os.path.join(sys.path[0] + '/../../../src'))

a = os.listdir(sys.path[-1])

from actions import empty_action, insert_value_to_list
from binary_solvers import DefaultBinarySolver
from dfsm.initiators import rules_providing, validators_providing
from dfsm.interfaces import BranchStateInterface, StateInterface, StateMapInterface
from dfsm.state_maps import DefaultStateMap
from elevator.additional_types import DoorsStates, ElevatorCommands
from elevator.branch_rule import BranchIsUniqueForStatesMap, IsClosingDoorsCorrect, IsMovingDownCorrect, IsMovingFromAvailableStage, IsMovingToAvailableStage, IsMovingUpCorrect, IsOpeningDoorsCorrect, MultyRule
from elevator.interfaces import DoorsStateHavingInterface, StageHavingInterface
from elevator.state_map_builder import DefaultStateMapGenerator
from elevator_brains.additional_types import Directions
from elevator_brains.elevator_brains import DefaultElevatorBrain
from elevator_brains.interfaces import DirectionHavingInterface, ElevatorCommandHavingInterface, FromStageHavingInterface, TaskQueueHavingInterface, ToStageHavingInterface
from elevator_brains.states import DefaultElevatorBrainState



scenarios("../features/features_elevator_brains/elevators_brain.feature")


@given(
    parsers.cfparse(
        'that max stage is {max_stage:value}.',
        extra_types={"value": int}
    ),
    target_fixture='max_stage'
)
def get_max_stage(max_stage: int):
    ioc.provide('Globals.Elevators', list())
    ioc.provide('Globals.MaxStage', max_stage)
    return max_stage


@given(
    parsers.cfparse(
        'that min stage is {min_stage:value}.',
        extra_types={"value": int}
    ),
    target_fixture='min_stage'
)
def get_min_stage(min_stage: int):
    ioc.provide('Globals.MinStage', min_stage)
    return min_stage


@given(
    parsers.cfparse(
        'requests queue:\n{requests_queue:value}',
        extra_types={"value": str}
    )
)
def get_requests_queue(requests_queue: int):
    rq = list()
    for i in json.loads(requests_queue):
        ri = Mock(spec=ToStageHavingInterface | FromStageHavingInterface | DirectionHavingInterface)
        ri.from_stage = i['from_stage']
        ri.to_stage = i['to_stage']
        ri.direction = Directions(i['direction'])
        rq.append(ri)
    ioc.provide('Globals.RequestsQueue', rq)


@given(
    parsers.cfparse(
        'elevator state map builded by this rules:\n{list_of_rules:value}',
        extra_types={"value": str}
    ),
    target_fixture='elevator_states_map'
)
def get_elevator_states_map(list_of_rules: str, min_stage: int, max_stage: int):

    ioc.provide('Constants.Building.MaxStage', max_stage)
    ioc.provide('Constants.Building.MinStage', min_stage)

    rules_names_interpritator = {
        'IsMovingToAvailableStage': IsMovingToAvailableStage(),
        'IsMovingFromAvailableStage': IsMovingFromAvailableStage(),
        'BranchIsUniqueForStatesMap': BranchIsUniqueForStatesMap(),
        'IsClosingDoorsCorrect': IsClosingDoorsCorrect(),
        'IsMovingUpCorrect': IsMovingUpCorrect(),
        'IsMovingDownCorrect': IsMovingDownCorrect(),
        'IsOpeningDoorsCorrect': IsOpeningDoorsCorrect(),
    }
    list_of_rules_processed = [rules_names_interpritator[rule_i] for rule_i in list_of_rules.split('\n')]
    
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

    mock_state_builder = mocked_state_builder_call
    mock_branch_builder = mocked_branch_state_builder_call
    mock_states_map_builder = mock_states_map_builder_call

    ioc.provide('Values.Get.Collection', lambda : list())
    ioc.provide('Rules.BranchRule', MultyRule(rules=list_of_rules_processed, aggregation_function=all))
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
    ioc.provide('Globals.StateMaps.ElevatorStateMap', states_map)


@given(
    parsers.cfparse(
        '{elevator_name:value1} elevator:\n{elevator_params:value2}',
        extra_types={"value1": str, "value2": str}
    )
)
def get_elevator(elevator_name, elevator_params):
    elevator_data = json.loads(elevator_params)
    elevator: StateInterface | DoorsStateHavingInterface | StageHavingInterface | DirectionHavingInterface | TaskQueueHavingInterface = Mock(
        spec=StateInterface | 
            DoorsStateHavingInterface | 
            StageHavingInterface | 
            DirectionHavingInterface |
            TaskQueueHavingInterface
    )
    elevator.stage = elevator_data['stage']
    elevator.direction = Directions(elevator_data['direction'])
    elevator.doors_state = DoorsStates(elevator_data['is_doors_opended'] == 'yes')
    elevator.task_queue = list()
    for ti in elevator_data['task_queue']:
        t = Mock(spec=ToStageHavingInterface | DirectionHavingInterface)
        t.to_stage = ti['to stage']
        t.direction = ti['direction']
        elevator.task_queue.append(t)
    elevator.__hash__ = lambda _: elevator_name.__hash__()
    elevator.__str__ = lambda _: elevator_name
    elevator.__eq__ = lambda _, s: elevator.stage == s.stage and elevator.doors_state == s.doors_state
    l = ioc.require('Globals.Elevators')
    l.append(elevator)


@given(
    parsers.cfparse(
        'elevators brains state map:\n{elevator_brain_state_map:value}',
        extra_types={"value": str}
    ),
    target_fixture='elevator_brain_state_map'
)
def get_elevator_brain_state_map(elevator_brain_state_map):
    branches = list()
    for ri in elevator_brain_state_map.split('\n')[1:]:
        is_doors_opened, is_finit_stage, is_required_stage, direction, elevator_command = ri.replace(' ', '')[1:-1].split('|')
        fs = DefaultElevatorBrainState(
            is_finit_stage=is_finit_stage=='yes',
            is_doors_opened=is_doors_opened=='yes',
            is_requered_stage=is_required_stage=='yes',
            direction=Directions(direction)
        )
        cmd = Mock(spec=ElevatorCommandHavingInterface)
        cmd.elevator_command = ElevatorCommands(elevator_command.replace('_', ' '))
        bi = Mock(spec=BranchStateInterface)
        bi.name = ''
        bi.from_state = fs
        bi.to_state = cmd
        branches.append(bi)
    a = DefaultStateMap(source_states_map=branches)
    ioc.provide('Globals.StateMaps.ElevatorsBrainStateMap', a)


@when(
    "updating elevators states by using DefaultElevatorsBrain."
)
def update_state():
    deb = DefaultElevatorBrain()
    deb()


@then(
    parsers.cfparse(
        'been gotted {elevator_name:value1} elevator:\n{expected_elevator_params:value2}',
        extra_types={"value1": str, "value2": str}
    )
)
def check_results(elevator_name, expected_elevator_params):
    l = ioc.require('Globals.Elevators')
    r = ioc.require('Globals.RequestsQueue')
    a = next(iter(filter(lambda a: a.__str__() == elevator_name, l)))
    elevator_data = json.loads(expected_elevator_params)
    assert a.stage == elevator_data['stage'], 'Incorrect stage'
    assert a.doors_state == DoorsStates(elevator_data['is_doors_opended'] == 'yes'), 'Incorrect doors state'
    k = 0
    for i in elevator_data['task_queue']:
        for j in a.task_queue:
            if i['to stage'] == j.to_stage and Directions(i['direction']) == j.direction:
                k += 1
                break
    jjjj = len(elevator_data['task_queue'])
    assert  k == jjjj, 'Incorrect task queue'

    
