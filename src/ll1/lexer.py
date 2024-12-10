import re
from src.ll1.constants import TOKENS_DICT


class Lexer:
    list_direct: list = list()
    symbol: str = ''
    tokens : list = list()
    
    
    def __init__(self, list_direct, symbol):
        Lexer.list_direct = list_direct
        Lexer.symbol = symbol
        Lexer.tokens = self.tokens
    

    def tokenize(self):
        self.symbol = re.sub(r'\s+', '', self.symbol)
        token_regex = '|'.join(f'(?P<{key}>{value})' for key, value in TOKENS_DICT.items())
        position = 0
        while position < len(self.symbol):
            ss = self.symbol[position:]
            match = re.match(token_regex, ss)
            kind = match.lastgroup
            value = match.group()
            Lexer.tokens.append(kind)
            position += len(value)
        Lexer.tokens.append('END')
