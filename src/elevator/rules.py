from typing import Any

import ioc
from dfsm.interfaces import StateRuleInterface, Stage
from elevator.additional_types import DoorsStates
from elevator.interfaces import DoorsStateHavingInterface, StageHavingInterface


class IsInAvailableStagesRule(StateRuleInterface):
    
    def __init__(self, max_stage: int, min_stage: int) -> None:
        self.max_stage = max_stage
        self.min_stage = min_stage
    

    def __call__(self, *args, **kwargs) -> bool:
        stage: int = ioc.require('Rules.ParamsExtractor.ExtractStage')(*args, **kwargs)
        return stage > self.min_stage and stage < self.max_stage


class IsDoorsOpen(StateRuleInterface):

    def __call__(self, *args, **kwargs) -> bool:
        doors_state: DoorsStates = ioc.require('Rules.ParamsExtractor.ExtractStage')(*args, **kwargs)
        return doors_state.doors_state == DoorsStates.opened
