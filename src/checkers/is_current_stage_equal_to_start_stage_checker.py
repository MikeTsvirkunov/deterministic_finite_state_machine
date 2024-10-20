from interfaces.current_stage_having_interface import CurrentStageHavingInterface
from interfaces.start_stage_having_interface import StartStageHavingInterface
from interfaces.rule_interface import RuleInterface


class IsCurrentStageEquealToStartStageChecker(RuleInterface):
    def __call__(self, *args, **kwds) -> bool:
        elevator: CurrentStageHavingInterface = kwds['elevator']
        task: StartStageHavingInterface = kwds['request']
        es = elevator.current_stage
        ts = task.start_stage
        return es == ts
