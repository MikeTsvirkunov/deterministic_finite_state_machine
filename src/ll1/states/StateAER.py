from src.ll1.lexer import Lexer
from src.ll1.condition import Consts
from src.ll1.states.IState import IState


class StateAER(IState):
    def __init__(self, curr, next, symbol):
        self.c = curr
        self.s = symbol
        self.next = next
    def transition(self):
        Lexer.must_error(Consts.TOKEN)
        Consts.TOKEN = Lexer.access(self.s)
        nxt = Consts.STACK.pop(-1)
        return nxt
