from typing import Callable, Collection, List
import ioc

from dfsm.interfaces import BranchStateInterface, StateInterface, StateMapInterface
from dfsm.state_maps import DefaultStateMap
from elevator.additional_types import DoorsStates, ElevatorCommands
from elevator.interfaces import DoorsStateHavingInterface, StageHavingInterface
from elevator_brains.actions import update_elevator_state
from elevator_brains.additional_types import Directions
from elevator_brains.constants import ELEVATOR_REQUEST_QUEUE_INSERT_SOLVER, ELEVATOR_TASK_QUEUE_CLEAN_SOLVER
from elevator_brains.interfaces import DirectionHavingInterface, ElevatorCommandHavingInterface, FromStageHavingInterface, IsFinitStageReachedInterface, TaskQueueHavingInterface
from elevator_brains.states import DefaultElevatorBrainState


class DefaultElevatorBrain:

    @staticmethod
    def is_finit_stage(elevator: TaskQueueHavingInterface | StageHavingInterface) -> bool:
        for ti in elevator.task_queue:
            if elevator.stage == ti.to_stage:
                return True
        return False


    @staticmethod
    def is_required_stage(elevator: TaskQueueHavingInterface | StageHavingInterface | DirectionHavingInterface) -> bool:
        list_of_requests: Collection[FromStageHavingInterface | DirectionHavingInterface] = ioc.require('Globals.RequestsQueue')
        for ri in list_of_requests:
            if elevator.stage == ri.from_stage and elevator.direction == ri.direction:
                return True
        return False


    @staticmethod
    def is_max_stage_achived(elevator: StageHavingInterface) -> bool:
        max_stage: int = ioc.require('Globals.MaxStage')
        return elevator.stage == max_stage


    @staticmethod
    def is_min_stage_achived(elevator: StageHavingInterface) -> bool:
        min_stage: int = ioc.require('Globals.MinStage')
        return elevator.stage == min_stage


    def __call__(self) -> None:
        
        elevator_state_map: StateMapInterface = ioc.require('Globals.StateMaps.ElevatorStateMap')
        elevator_brain_state_map: StateMapInterface = ioc.require('Globals.StateMaps.ElevatorsBrainStateMap')
        elevators: Collection[
            DirectionHavingInterface | 
            TaskQueueHavingInterface |  
            StateInterface | 
            DoorsStateHavingInterface
        ] = ioc.require('Globals.Elevators')
        
        for ei in elevators:

            a = ei.__str__()
            l = ioc.require('Globals.RequestsQueue')
            is_finit_stage_i: bool = DefaultElevatorBrain.is_finit_stage(elevator=ei)
            is_required_stage_i: bool = DefaultElevatorBrain.is_required_stage(elevator=ei)
            is_max_stage_achived_i: bool = DefaultElevatorBrain.is_max_stage_achived(elevator=ei)
            is_min_stage_achived_i: bool = DefaultElevatorBrain.is_min_stage_achived(elevator=ei) 

            direction: Directions = ei.direction
            s: DefaultElevatorBrainState = DefaultElevatorBrainState(
                is_finit_stage=is_finit_stage_i,
                is_requered_stage=is_required_stage_i,
                is_doors_opened=ei.doors_state == DoorsStates.opened,
                direction=direction
            )
            cmd: ElevatorCommandHavingInterface = elevator_brain_state_map.next(
                branch_name='',
                state=s
            )
            is_empty: bool = len(ei.task_queue) == 0

            next_elevator_state = elevator_state_map.next(cmd.elevator_command, ei)
            update_elevator_state(
                elevator=ei,
                next_elevator_state=next_elevator_state,
                is_finit_stage=is_finit_stage_i,
                is_required_stage=is_required_stage_i,
                is_max_stage_achived=is_max_stage_achived_i,
                is_min_stage_achived=is_min_stage_achived_i,
                is_empty=is_empty
            )
