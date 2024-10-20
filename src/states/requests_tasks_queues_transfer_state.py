from interfaces.state_interface import StateInterface


class RequestsTasksQueuesTransferState(StateInterface):
    def __init__(
        self,
        is_request_queue_empty: bool,
        is_directions_equal: bool,
        is_stage_equals: bool,
    ):
        self.is_request_queue_empty = is_request_queue_empty
        self.is_stage_equals = is_stage_equals
        self.is_directions_equal = is_directions_equal


    def __str__(self):
        return f'is_request_queue_empty: {self.is_request_queue_empty},' +\
                f' is_request_queue_empty: {self.is_stage_equals},' +\
                f' is_request_queue_empty: {self.is_request_queue_empty}'


    def __hash__(self) -> int:
        hash_data = str(self).__hash__()
        return hash_data
    

    def __eq__(self, other):
        return all([
            self.is_request_queue_empty == other.is_request_queue_empty,
            self.is_stage_equals == other.is_stage_equals,
            self.is_directions_equal == other.is_directions_equal
        ])