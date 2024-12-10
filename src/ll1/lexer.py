import re
from src.ll1.constants import TOKENS_DICT
from src.ll1.condition import Consts


class Lexer:
    list_direct: list = list()
    symbol: str = ''
    tokens : list = list()
    def __init__(self, list_direct, symbol):
        Lexer.list_direct = list_direct
        Lexer.symbol = symbol
        Lexer.tokens = self.get_tokens()
        
    def tokenize(self):
        self.symbol = re.sub(r'\s+', '', self.symbol)
        token_regex = '|'.join(f'(?P<{key}>{value})' for key, value in TOKENS_DICT.items())
        position = 0
        while position < len(self.symbol):
            ss = self.symbol[position:]
            match = re.match(token_regex, ss)
            if match:
                kind = match.lastgroup
                value = match.group()
                if kind:
                    Lexer.tokens.append(kind)
                position += len(value)
            else:
                raise ValueError(f"Ошибка: не найдено ни одного токена в строке. Необработанный символ: '{self.symbol[position]}'")

        Lexer.tokens.append('END')
    
    
    def get_tokens(self):
        return Lexer.tokens
    
    @staticmethod
    def access(s):
        if Consts.INDEX < len(Lexer.tokens):
            Consts.INDEX += 1
            s = Lexer.tokens[Consts.INDEX]
        else:
            s = None
        return s
        
    @staticmethod
    def must_error(s):
        def raise_syntax_error(symbol):
            raise SyntaxError(f"Символ '{symbol}' не найден в списке.")

        must_error = lambda: (s in Lexer.list_direct) or raise_syntax_error(Lexer.symbol)
        must_error()
