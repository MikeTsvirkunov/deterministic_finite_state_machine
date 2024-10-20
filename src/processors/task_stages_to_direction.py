from custom_types.directions import Directions
from interfaces.finit_stage_having_interface import FinitStageHavingInterface
from interfaces.start_stage_having_interface import StartStageHavingInterface


def taskStagesToDirection(task: FinitStageHavingInterface | StartStageHavingInterface):
    if task.finit_stage > task.finit_stage:
        return Directions.up
    else:
        return Directions.down
