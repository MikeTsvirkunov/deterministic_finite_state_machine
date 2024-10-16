from interfaces.current_stage_having_interface import CurrentStageHavingInterface
from interfaces.is_door_open_interface import IsDoorOpenInterface
from interfaces.rule_interface import RuleInterface


class IsNotMovingWithOpenDoorsRule(RuleInterface):
    def __call__(self, data) -> bool:
        current_state: CurrentStageHavingInterface | IsDoorOpenInterface = data[0]
        next_state: CurrentStageHavingInterface | IsDoorOpenInterface = data[1]
        is_stage_change = current_state.current_stage != next_state.current_stage
        is_door_state_changed = current_state.is_door_open != next_state.is_door_open
        is_door_open = current_state.is_door_open
        res = (not is_stage_change) or (is_stage_change and (not is_door_state_changed) and (not is_door_open))
        return res