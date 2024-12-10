from src.ll1.lexer import Lexer
from src.ll1.states.IState import IState

class StateN(IState):
    def __init__(self, curr, next, symbol):
        self.c = curr
        self.s = symbol
        self.next = next
    def transition(self):
        result = lambda: self.next if self.s in Lexer.list_direct else self.c + 1
        return result()
