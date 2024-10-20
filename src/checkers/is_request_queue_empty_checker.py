from typing import Iterable
import ioc
from interfaces.rule_interface import RuleInterface


class IsRequestQueueEmptyChecker(RuleInterface):
    def __call__(self, *args, **kwds) -> bool:
        request_queue: Iterable = ioc.require('Variables.RequestsQueue') 
        return request_queue.empty()
