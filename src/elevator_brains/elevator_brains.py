import ioc

from dfsm.interfaces import StateMapInterface
from elevator.interfaces import StageHavingInterface
from elevator_brains.interfaces import DirectionHavingInterface, TaskQueueHavingInterface


class DefaultElevatorBrain:
     

     def __call__(self) -> None:
        commands_states_map: StateMapInterface = ioc.require('Globals.Comands.StatesMap')
        max_stage: int = int(ioc('Globals.'))
        elevators = ioc.require('Globals.Elevators')
        for elevator_i in elevators:
            e: DirectionHavingInterface | TaskQueueHavingInterface | StageHavingInterface = elevator_i
            
            
            
