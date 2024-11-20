from dfsm.interfaces import StateInterface
from elevator.additional_types import ElevatorCommands
from elevator_brains.additional_types import Directions


class DefaultElevatorBrainState(StateInterface):
    def __init__(
        self, 
        is_finit_stage: bool, 
        is_requered_stage: bool,
        is_doors_opened: bool,
        direction: Directions
    ) -> None:
        self.is_finit_stage = is_finit_stage
        self.is_requered_stage = is_requered_stage
        self.direction = direction
        self.is_doors_opened = is_doors_opened
    

    def __hash__(self):
        a = '__'.join([
            str(self.is_finit_stage),
            str(self.is_requered_stage),
            str(self.is_doors_opened),
            str(self.direction)
        ])
        return a
    

    def __eq__(self, value):
        a1 = self.is_finit_stage == value.is_finit_stage
        a2 = self.is_requered_stage == value.is_requered_stage
        a4 = self.is_doors_opened == value.is_doors_opened
        a5 = self.direction == value.direction
        return all([a1, a2, a4, a5])
        