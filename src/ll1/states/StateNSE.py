from src.ll1.lexer import Lexer
from src.ll1.condition import Consts
from src.ll1.states.IState import IState


class StateNSE(IState):
    def __init__(self, curr, next, symbol):
        self.c = curr
        self.s = symbol
        self.next = next
    def transition(self):
        Consts.STACK.append(self.c + 1)
        Lexer.must_error(self.s)
        return self.next
