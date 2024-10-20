from actors.empty_actor import EmptyActor
from actors.requests_tasks_queues_transfer_actor import RequestsTasksQueuesTransferActor
from actors.task_queue_add_actor import TaskQueueAddActor
from states.requests_tasks_queues_transfer_state import RequestsTasksQueuesTransferState


REQUESTS_TASKS_QUEUES_TRANSFER_STATE_MAPPER = {

    RequestsTasksQueuesTransferState(
        is_request_queue_empty=True,
        is_directions_equal=True,
        is_stage_equals=True,
    ): EmptyActor(),
    RequestsTasksQueuesTransferState(
        is_request_queue_empty=True,
        is_directions_equal=False,
        is_stage_equals=True,
    ): EmptyActor(),
    RequestsTasksQueuesTransferState(
        is_request_queue_empty=True,
        is_directions_equal=True,
        is_stage_equals=False,
    ): EmptyActor(),
    RequestsTasksQueuesTransferState(
        is_request_queue_empty=True,
        is_directions_equal=False,
        is_stage_equals=False,
    ): EmptyActor(),

    RequestsTasksQueuesTransferState(
        is_request_queue_empty=False,
        is_directions_equal=False,
        is_stage_equals=False,
    ): EmptyActor(),
    RequestsTasksQueuesTransferState(
        is_request_queue_empty=False,
        is_directions_equal=False,
        is_stage_equals=True,
    ): EmptyActor(),
    RequestsTasksQueuesTransferState(
        is_request_queue_empty=False,
        is_directions_equal=True,
        is_stage_equals=False,
    ): EmptyActor(),

    RequestsTasksQueuesTransferState(
        is_request_queue_empty=False,
        is_directions_equal=True,
        is_stage_equals=True,
    ): TaskQueueAddActor(),
}