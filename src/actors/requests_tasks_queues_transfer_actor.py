from typing import Callable
import ioc
from interfaces.actor_interface import ActorInterface
from interfaces.current_stage_having_interface import CurrentStageHavingInterface
from interfaces.direction_having_interface import DirectionHavingInterface
from interfaces.start_stage_having_interface import StartStageHavingInterface
from interfaces.task_queue_having_interface import TaskQueueHavingInterface


class RequestsTasksQueuesTransferActor(ActorInterface):
    def __call__(self, *args, **kwds) -> None:
        state_builder: Callable = ioc.require('Bulders.RequestsTasksQueuesTransferStateBuilder')
        state_mapper: Callable = ioc.require('Bulders.RequestsTasksQueuesTransferStateMapper')
        elevator: DirectionHavingInterface | CurrentStageHavingInterface | TaskQueueHavingInterface = kwds['elevator']
        request_queue = ioc.require('Variables.RequestsQueue')
        noi = len(request_queue)
        for idx in range(noi):
            request: DirectionHavingInterface | StartStageHavingInterface = request_queue[idx]
            state = state_builder(elevator=elevator, request=request)
            state_actor = state_mapper[state]
            state_actor(elevator=elevator, request_idx=idx)
            