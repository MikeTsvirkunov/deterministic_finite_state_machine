from interfaces.rule_interface import RuleInterface


class IsMovingByDirectionChecker(RuleInterface):
    def __call__(self, *args, **kwds) -> bool:
        ed = kwds['elevator'].direction
        td = kwds['task'].direction
        return td == ed
