import ioc
from ll1.interfaces import ApplyStrategyInterface
from ll1.lexer import Lexer
from typing import Collection


def checking_access() -> str:
    index: int = ioc.require('LL1_GRAMMAR.globals.index')
    tokens: Collection[str] = ioc.require('LL1_GRAMMAR.globals.tokens')
    if index < len(tokens):
        index += 1
        ioc.provide("LL1_GRAMMAR.globals.token", tokens[index])
    ioc.provide("LL1_GRAMMAR.globals.token", None)


def checking_error() -> None:
    token: str = ioc.require('LL1_GRAMMAR.globals.token')
    list_direct: str = ioc.require('LL1_GRAMMAR.globals.list_direct')
    if token not in list_direct:
        raise SyntaxError(f"Символ '{token}' не найден в списке.")


# Lastless
class AcceptNext(ApplyStrategyInterface):
    
    @staticmethod
    def __call__(current_idx: int, next_idx: int) -> int:
        tokens: Collection[str] = ioc.require('LL1_GRAMMAR.globals.tokens')
        index: int = ioc.require('LL1_GRAMMAR.globals.index')
        index += 1
        ioc.provide("LL1_GRAMMAR.globals.token", tokens[index])
        return next_idx


class AcceptErrorReturn(ApplyStrategyInterface):
    
    @staticmethod
    def __call__(current_idx: int, next_idx: int) -> int:
        checking_access()
        checking_error()
        return next_idx
    

class ErrorReturn(ApplyStrategyInterface):
    
    @staticmethod
    def __call__(current_idx: int, next_idx: int) -> int:
        checking_error()
        stack = ioc.require('LL1_GRAMMAR.globals.stack')
        next_idx = stack.pop(-1)
        ioc.provide('LL1_GRAMMAR.globals.stack', stack)
        return next_idx
    

class Next(ApplyStrategyInterface):
    
    @staticmethod
    def __call__(current_idx: int, next_idx: int) -> int:
        token: str = ioc.require('LL1_GRAMMAR.globals.token')
        list_direct: str = ioc.require('LL1_GRAMMAR.globals.list_direct')
        if token in list_direct:
            return next_idx
        else:
            current_idx + 1


class AcceptErrorNext(ApplyStrategyInterface):
    
    @staticmethod
    def __call__(current_idx: int, next_idx: int) -> int:
        checking_access()
        checking_error()
        return next_idx


class ErrorNext(ApplyStrategyInterface):
    
    @staticmethod
    def __call__(current_idx: int, next_idx: int) -> int:
        checking_access()
        return next_idx


class ErrorStackNext(ApplyStrategyInterface):
    
    @staticmethod
    def __call__(current_idx: int, next_idx: int) -> int:
        checking_error()
        stack = ioc.require('LL1_GRAMMAR.globals.stack')
        stack.append(current_idx + 1)
        ioc.provide('LL1_GRAMMAR.globals.stack', stack)
        return next_idx