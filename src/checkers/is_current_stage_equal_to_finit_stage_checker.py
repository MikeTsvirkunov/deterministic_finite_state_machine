from interfaces.current_stage_having_interface import CurrentStageHavingInterface
from interfaces.finit_stage_having_interface import FinitStageHavingInterface
from interfaces.rule_interface import RuleInterface


class IsCurrentStageEquealToFinitStageChecker(RuleInterface):
    def __call__(self, *args, **kwds) -> bool:
        elevator: CurrentStageHavingInterface = kwds['elevator']
        task: FinitStageHavingInterface = kwds['task']
        es = elevator.current_stage
        ts = task.finit_stage
        return es == ts
