from typing import Callable, Iterator
import ioc
from interfaces.actor_interface import ActorInterface
from interfaces.current_stage_having_interface import CurrentStageHavingInterface
from interfaces.direction_having_interface import DirectionHavingInterface
from interfaces.start_stage_having_interface import StartStageHavingInterface
from interfaces.task_queue_having_interface import TaskQueueHavingInterface


class TaskQueueAddActor(ActorInterface):
    def __call__(self, *args, **kwds) -> None:
        idx: int = kwds['request_idx']
        request_queue: Iterator = ioc.require('Variables.RequestsQueue')
        elevator: TaskQueueHavingInterface = kwds['elevator']
        value = request_queue.pop(idx)
        elevator.task_queue.append(value)
