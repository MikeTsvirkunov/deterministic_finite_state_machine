from typing import Callable, Collection
import ioc
from binary_solvers import BinarySolverInterface
from dfsm.interfaces import BranchStateInterface, RuleInterface, StateInterface, StateMapInterface
from itertools import product

from elevator.additional_types import DoorsStates, ElevatorCommands


class DefaultStateMapGenerator:
    @staticmethod
    def __call__(max_stage, min_stage) -> StateMapInterface:
        state_builder: Callable[[int, DoorsStates], StateInterface] = ioc.require('Builders.ElevatorState.Builder.Default')
        branch_builder: Callable[[ElevatorCommands, StateInterface, StateInterface], BranchStateInterface] = ioc.require('Builders.ElevatorBranchState.Builder.Default')
        states_map_builder: Callable[[Collection[BranchStateInterface]], StateMapInterface] = ioc.require('Builders.StatesMap.Default')
        states_map: Collection[BranchStateInterface] = ioc.require('Values.Get.Collection')()
        rule_for_branch: RuleInterface = ioc.require('Rules.BranchRule')
        validate_append: BinarySolverInterface = ioc.require('Validators.InsertCorrectBranch')

        for (
            branch_name, 
            stage_1, 
            doors_state_1, 
            stage_2, 
            doors_state_2
        ) in product(
            ElevatorCommands,
            range(min_stage, max_stage+1),
            DoorsStates,
            range(min_stage, max_stage+1),
            DoorsStates
        ):
            from_state: StateInterface = state_builder(stage=stage_1, doors_state=doors_state_1)
            to_state: StateInterface = state_builder(stage=stage_2, doors_state=doors_state_2)
            branch: BranchStateInterface = branch_builder(branch_name=branch_name, from_state=from_state, to_state=to_state)
            # рефлексирующие программные системы
            res: bool = rule_for_branch(branch=branch, states_map=states_map)
            valid_action: Callable = validate_append(res)
            valid_action(states_map, branch)
        return states_map_builder(states_map=states_map)
