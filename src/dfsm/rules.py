from typing import Callable
from dfsm.interfaces import StateRuleInterface, RulesHavingInterface, StateInterface


class MultyRule(StateRuleInterface, RulesHavingInterface):

    def __init__(self, rules, aggregation_function: Callable = all):
        self.rules = rules
        self.aggregation_function = aggregation_function
    
    def __call__(self, state: StateInterface) -> bool:
        return self.aggregation_function(map(lambda f: f(state), self.rules))