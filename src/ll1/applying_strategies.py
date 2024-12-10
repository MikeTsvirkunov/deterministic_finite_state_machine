import ioc
from src.ll1.interfaces import ApplyStrategyInterface

def checking_access() -> str:
    index: int = int(ioc.require('LL1_GRAMMAR.globals.index'))
    tokens: list[str] = list(ioc.require('LL1_GRAMMAR.globals.tokens'))
    index += 1
    ioc.override('LL1_GRAMMAR.globals.index', index)
    return tokens[index]


def checking_error() -> None:
    token: str = str(ioc.require('LL1_GRAMMAR.globals.token'))
    list_direct: list[str] = list(ioc.require('LL1_GRAMMAR.globals.list_direct'))
    if token not in list_direct:
        raise SyntaxError(f"Символ '{token}' не найден в списке.")


class AcceptNext(ApplyStrategyInterface):
        
    @staticmethod
    def __call__(current_idx: int, next_idx: int) -> int:
        new_token = checking_access()
        ioc.override("LL1_GRAMMAR.globals.token", new_token)
        return next_idx


class AcceptErrorReturn(ApplyStrategyInterface):
    
    @staticmethod
    def __call__(current_idx: int, next_idx: int) -> int:
        checking_error()
        new_token = checking_access()
        ioc.override("LL1_GRAMMAR.globals.token", new_token)
        stack: list[int] = list(ioc.require('LL1_GRAMMAR.globals.stack'))
        next_idx = stack.pop(-1)
        ioc.override('LL1_GRAMMAR.globals.stack', stack)
        return next_idx
    

class ErrorReturn(ApplyStrategyInterface):
    
    @staticmethod
    def __call__(current_idx: int, next_idx: int) -> int:
        checking_error()
        stack = list(ioc.require('LL1_GRAMMAR.globals.stack'))
        next_idx = stack.pop(-1)
        ioc.override('LL1_GRAMMAR.globals.stack', stack)
        return next_idx
    

class Next(ApplyStrategyInterface):
    
    @staticmethod
    def __call__(current_idx: int, next_idx: int) -> int:
        token: str = ioc.require('LL1_GRAMMAR.globals.token')
        list_direct: str = ioc.require('LL1_GRAMMAR.globals.list_direct')
        if token in list_direct:
            return next_idx
        else:
            return current_idx + 1


class AcceptErrorNext(ApplyStrategyInterface):
    
    @staticmethod
    def __call__(current_idx: int, next_idx: int) -> int:
        checking_error()
        new_token = checking_access()
        ioc.override("LL1_GRAMMAR.globals.token", new_token)
        return next_idx


class ErrorNext(ApplyStrategyInterface):
    
    @staticmethod
    def __call__(current_idx: int, next_idx: int) -> int:
        checking_error()
        return next_idx


class ErrorStackNext(ApplyStrategyInterface):
    
    @staticmethod
    def __call__(current_idx: int, next_idx: int) -> int:
        checking_error()
        stack: list[int] = list(ioc.require('LL1_GRAMMAR.globals.stack'))
        stack.append(current_idx + 1)
        ioc.override('LL1_GRAMMAR.globals.stack', stack)
        return next_idx