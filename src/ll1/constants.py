import json


TOKENS_DICT = {
    # Eps
    'eps': r'eps',
    # Arg
    'BOOL': r'(true|false)+',
    'FUNCTION_NAME': r'[a-zA-Z][a-zA-Z0-9]*',
    'NUMERIC': r'[0-9]+',
    'SEPARATOR': r'\,',
    # Brackets
    'LPAR': r'\(',
    'RPAR': r'\)',
    # Ariphmetics
    'MUT': r'\*',
    'REMUT': r'\/',
    'SUM': r'\+',
    'DELTA': r'\-',
    # Boolean
    'AND': r'\&',
    'OR': r'\|',
    'NOT': r'\!',
    # Compear
    'LARGER': r'\>',
    'BIGGER': r'\<',
    'BEQUAL': r'\=',
    # Specific
    'if': r'if',
    'resolve': r'resolve',
    'foreach': r'foreach',
    'equal': r'equal',
}


with open('data/transaction.json') as f:
    TRANSITIONS = {int(i): j for i, j in json.load(f).items()}
