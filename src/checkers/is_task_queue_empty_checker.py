from interfaces.rule_interface import RuleInterface
from interfaces.task_queue_having_interface import TaskQueueHavingInterface


class IsTaskQueueEmptyChecker(RuleInterface):
    def __call__(self, *args, **kwds) -> bool:
        elevator: TaskQueueHavingInterface = kwds['elevator']
        return len(elevator.task_queue) == 0
