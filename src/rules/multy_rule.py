from typing import Any, Iterable
from interfaces.rule_interface import RuleInterface


class MultyRule(RuleInterface):
    
    def __init__(self, list_of_rules: Iterable[RuleInterface]) -> None:
        self.list_of_rules = list_of_rules 

    def __call__(self, data: Any) -> bool:
        res = list(map(lambda f: f(data), self.list_of_rules))
        res = all(res)
        return res