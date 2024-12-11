from enum import Enum
import re
import ioc

from src.ll1.constants import TOKENS_DICT


class ExecutingCodes(int, Enum):
    success_code: int = 1
    invalid_sintax_code: int = 2
    none: int = 0


def get_state_vector():
    action = str(ioc.require('LR1.current_step.action'))
    return (
        int(action == None),
        int(action.startswith('s')),
        int(action.startswith('r')),
        int(action == 'acc')
    )



def parse_row(symbol):
    symbol = re.sub(r'\s+', '', symbol)
    tokens = list()
    token_regex = '|'.join(f'(?P<{key}>{value})' for key, value in TOKENS_DICT.items())
    position = 0
    while position < len(symbol):
        ss = symbol[position:]
        match = re.match(token_regex, ss)
        kind = match.lastgroup
        value = match.group()
        tokens.append(kind)
        position += len(value)
    return tokens


def lr1_parcer_initiation():
    ioc.override('LR1.globals.stack', [0])
    ioc.override('LR1.globals.cursor', 0)
    ioc.override('LR1.globals.is_success', ExecutingCodes.none)


def provide_grammar(grammar: list[str, list[str]], parsing_table: dict):
    ioc.override('LR1.globals.parsing_table', parsing_table)
    ioc.require('LR1.globals.grammar', grammar)


def provide_input_string(row: list[str]):
    ioc.override('LR1.globals.input_string', row + ['$'])


def step_initiation():
    input_string = list(ioc.require('LR1.globals.input_string'))
    stack = list(ioc.require('LR1.globals.stack'))
    cursor = int(ioc.require('LR1.globals.cursor'))
    parsing_table = dict(ioc.require('LR1.globals.parsing_table'))
    state = stack[-1]
    current_token = input_string[cursor]
    action = parsing_table[state].get(current_token, None)
    ioc.override('LR1.current_step.action', action)
    ioc.override('LR1.current_step.current_token', current_token)



def extract_idx_from_action(action: str):
    return int(action[1:])


def increment_cursor():
    cursor = int(ioc.require('LR1.globals.cursor'))
    cursor += 1
    ioc.override('LR1.globals.cursor', cursor)


def get_production():
    grammar = list(ioc.require('LR1.globals.grammar'))
    action = str(ioc.require('LR1.current_step.action'))
    idx = extract_idx_from_action(action)
    return grammar[idx]


def s_action():
    stack = list(ioc.require('LR1.globals.stack'))
    action = str(ioc.require('LR1.current_step.action'))
    current_token = str(ioc.require('LR1.current_step.current_token'))
    stack.append(current_token)
    stack.append(extract_idx_from_action(action))
    increment_cursor()
    ioc.override('LR1.globals.stack', stack)


def r_action():
    stack = list(ioc.require('LR1.globals.stack'))
    parsing_table = dict(ioc.require('LR1.globals.parsing_table'))
    production = get_production()
    for _ in range(2 * len(production[1])):
        stack.pop()
    state = stack[-1]
    stack.append(production[0])
    stack.append(parsing_table[state][production[0]])
    ioc.override('LR1.globals.stack', stack)


def success_acccept_action():
    ioc.override('LR1.globals.is_success', ExecutingCodes.success_code)


def error_acccept_action():
    ioc.override('LR1.globals.is_success', ExecutingCodes.invalid_sintax_code)
