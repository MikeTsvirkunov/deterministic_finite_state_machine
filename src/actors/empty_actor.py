from typing import Callable
import ioc
from interfaces.actor_interface import ActorInterface
from interfaces.current_stage_having_interface import CurrentStageHavingInterface
from interfaces.direction_having_interface import DirectionHavingInterface
from interfaces.start_stage_having_interface import StartStageHavingInterface
from interfaces.task_queue_having_interface import TaskQueueHavingInterface


class EmptyActor(ActorInterface):
    def __call__(self, *args, **kwds) -> None:
        print()
        pass
            