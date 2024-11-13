from typing import Callable, Collection

import ioc
from dfsm.interfaces import RuleInterface, BranchStateInterface
from elevator.additional_types import DoorsStates, ElevatorCommands
from elevator.interfaces import DoorsStateHavingInterface, StageHavingInterface


class IsMovingWithClosedDoors(RuleInterface):

    def __call__(self, *args, **kwargs) -> bool:
        branch: BranchStateInterface = kwargs['branch']
        doors_state_1: DoorsStateHavingInterface = branch.from_state
        doors_state_2: DoorsStateHavingInterface = branch.to_state

        stage_state_1: StageHavingInterface = branch.from_state
        stage_state_2: StageHavingInterface = branch.to_state

        is_moved = stage_state_1.stage != stage_state_2.stage
        is_doors_closed_1 = doors_state_1.doors_state == DoorsStates.closed
        is_doors_closed_2 = doors_state_2.doors_state == DoorsStates.closed
        
        return (
            is_moved and is_doors_closed_1 and is_doors_closed_2
        ) or (
            (not is_moved) and is_doors_closed_1 and (not is_doors_closed_2)
        ) or (
            (not is_moved) and (not is_doors_closed_1) and is_doors_closed_2
        ) or (
            (not is_moved) and (not is_doors_closed_1) and (not is_doors_closed_2)
        )


class IsMovingOnOnlyOneStage(RuleInterface):

    def __call__(self, *args, **kwargs) -> bool:
        branch: BranchStateInterface = kwargs['branch']
        stage_state_1: StageHavingInterface = branch.from_state
        stage_state_2: StageHavingInterface = branch.to_state
        return abs(stage_state_1.stage - stage_state_2.stage) <= 1


class IsDoorsClosed(RuleInterface):

    def __call__(self, *args, **kwargs) -> bool:
        branch: BranchStateInterface = kwargs['branch']
        branch_name: ElevatorCommands = branch.name
        doors_state_1: DoorsStateHavingInterface = branch.from_state
        doors_state_2: DoorsStateHavingInterface = branch.to_state
        is_doors_closed_1 = doors_state_1.doors_state == DoorsStates.closed
        is_doors_closed_2 = doors_state_2.doors_state == DoorsStates.closed
        
        return (
            is_doors_closed_1 and is_doors_closed_2
        ) or (
            (not is_doors_closed_1) and is_doors_closed_2
        ) or (
            is_doors_closed_1 and (not is_doors_closed_2)
        )


class IsClosingDoorsCorrect(RuleInterface):
    
    def __call__(self, *args, **kwargs) -> bool:
        branch: BranchStateInterface = kwargs['branch']
        command: ElevatorCommands = branch.name
        stage_state_1: StageHavingInterface = branch.from_state
        stage_state_2: StageHavingInterface = branch.to_state
        doors_state_1: DoorsStateHavingInterface = branch.from_state
        doors_state_2: DoorsStateHavingInterface = branch.to_state
        is_doors_opened_1 = doors_state_1.doors_state == DoorsStates.opened
        is_doors_closed_2 = doors_state_2.doors_state == DoorsStates.closed
        
        is_command_correct = command == ElevatorCommands.close_doors
        is_stage_not_changed = stage_state_1.stage == stage_state_2.stage

        return (
            is_command_correct 
            and 
            is_doors_opened_1 
            and 
            is_doors_closed_2 
            and 
            is_stage_not_changed
        ) or (
            not is_command_correct
        )


class IsOpeningDoorsCorrect(RuleInterface):
    
    def __call__(self, *args, **kwargs) -> bool:
        branch: BranchStateInterface = kwargs['branch']
        command: ElevatorCommands = branch.name

        doors_state_1: DoorsStateHavingInterface = branch.from_state
        doors_state_2: DoorsStateHavingInterface = branch.to_state
        is_doors_closed_1 = doors_state_1.doors_state == DoorsStates.closed
        is_doors_opend_2 = doors_state_2.doors_state == DoorsStates.opened
        
        stage_state_1: StageHavingInterface = branch.from_state
        stage_state_2: StageHavingInterface = branch.to_state
        
        is_command_correct = command == ElevatorCommands.open_doors
        is_stage_not_changed = stage_state_1.stage == stage_state_2.stage
        return (
            is_command_correct 
            and 
            is_doors_closed_1 
            and 
            is_doors_opend_2
            and
            is_stage_not_changed
        ) or (
            not is_command_correct
        )


class IsMovingUpCorrect(RuleInterface):
    
    def __call__(self, *args, **kwargs) -> bool:
        branch: BranchStateInterface = kwargs['branch']
        command: ElevatorCommands = branch.name

        doors_state_1: DoorsStateHavingInterface = branch.from_state
        doors_state_2: DoorsStateHavingInterface = branch.to_state
        is_doors_closed_1 = doors_state_1.doors_state == DoorsStates.closed
        is_doors_closed_2 = doors_state_2.doors_state == DoorsStates.closed
        stage_state_1: StageHavingInterface = branch.from_state
        stage_state_2: StageHavingInterface = branch.to_state
        
        is_command_correct = command == ElevatorCommands.move_up
        is_moved_up = (stage_state_2.stage - stage_state_1.stage) == 1

        return (
            is_command_correct 
            and 
            is_doors_closed_1 
            and 
            is_doors_closed_2 
            and 
            is_moved_up
        ) or (
            not is_command_correct
        )


class IsMovingDownCorrect(RuleInterface):
    
    def __call__(self, *args, **kwargs) -> bool:
        branch: BranchStateInterface = kwargs['branch']
        command: ElevatorCommands = branch.name

        doors_state_1: DoorsStateHavingInterface = branch.from_state
        doors_state_2: DoorsStateHavingInterface = branch.to_state
        is_doors_closed_1 = doors_state_1.doors_state == DoorsStates.closed
        is_doors_closed_2 = doors_state_2.doors_state == DoorsStates.closed
        stage_state_1: StageHavingInterface = branch.from_state
        stage_state_2: StageHavingInterface = branch.to_state
        
        is_command_correct = command == ElevatorCommands.move_down
        is_moved_down = (stage_state_1.stage - stage_state_2.stage) == 1

        return (
            is_command_correct 
            and 
            is_doors_closed_1 
            and 
            is_doors_closed_2 
            and 
            is_moved_down
        ) or (
            not is_command_correct
        )


class IsMovingToAvailableStage(RuleInterface):

    def __call__(self, *args, **kwargs) -> bool:
        branch: BranchStateInterface = kwargs['branch']
        max_stage: int = int(ioc.require('Constants.Building.MaxStage'))
        min_stage: int = int(ioc.require('Constants.Building.MinStage'))

        stage_state_2: StageHavingInterface = branch.to_state
        r1 = stage_state_2.stage >= min_stage
        r2 = stage_state_2.stage <= max_stage
        return r1 and r2


class IsMovingFromAvailableStage(RuleInterface):

    def __call__(self, *args, **kwargs) -> bool:
        branch: BranchStateInterface = kwargs['branch']
        max_stage: int = int(ioc.require('Constants.Building.MaxStage'))
        min_stage: int = int(ioc.require('Constants.Building.MinStage'))

        stage_state_1: StageHavingInterface = branch.from_state

        return stage_state_1.stage >= min_stage and stage_state_1.stage <= max_stage


class BranchIsUniqueForStatesMap(RuleInterface):
    def __call__(self, *args, **kwargs) -> bool:
        branch: BranchStateInterface = kwargs['branch']
        states_map: Collection[BranchStateInterface] = kwargs['states_map']
        return all([
            (
                branch_i.from_state != branch.from_state
                or
                branch_i.to_state != branch.to_state
                or
                branch_i.name != branch.name
            ) for branch_i in states_map
        ])


class MultyRule(RuleInterface):

    def __init__(self, rules: Collection[RuleInterface], aggregation_function: Callable) -> None:
        self.rules = rules
        self.aggregation_function = aggregation_function


    def __call__(self, *args, **kwargs) -> bool:
        r = [rule_i(*args, **kwargs) for rule_i in self.rules]
        return self.aggregation_function(r)
