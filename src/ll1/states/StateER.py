from src.ll1.lexer import Lexer
from src.ll1.states.IState import IState
from src.ll1.condition import Consts

class StateER(IState):
    def __init__(self, curr, next, symbol):
        self.c = curr
        self.s = symbol
        self.next = next
    def transition(self):
        Lexer.must_error(self.s)
        nxt = Consts.STACK.pop()
        return nxt
