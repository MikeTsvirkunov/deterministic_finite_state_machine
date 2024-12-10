import json
from typing import Dict, Tuple
import ioc
import pandas as pd
import pytest
import sys
sys.path.append(sys.path[0] + '\\..\\')
from src.ll1.applying_strategies import AcceptErrorNext, AcceptErrorReturn, AcceptNext, ErrorNext, ErrorReturn, ErrorStackNext, Next
from src.ll1.interfaces import ApplyStrategyInterface
from src.ll1.lexer import Lexer
from src.ll1.constants import TRANSITIONS


def get_next_idx_from_table(table: pd.DataFrame, current_idx: int):
    return table.loc[current_idx, 'NEXT']


def get_follow_symbols_from_table(table: pd.DataFrame, current_idx: int):
    v = table.loc[current_idx, 'FOLLOW_SYMBOLS'].replace(
        '\'', ''
    ).replace(
        '[', ''
    ).replace(
        ']', ''
        ).split(', ')
    return tuple(v)


def get_state_vector_from_table(table: pd.DataFrame, current_idx: int):
    return tuple(table.loc[current_idx, ['ACCEPT','STACK','ERROR','RETURN']].tolist())

def initiation():
    ioc.provide("LL1_GRAMMAR.globals.token", None)
    ioc.provide("LL1_GRAMMAR.globals.tokens", list())
    ioc.provide("LL1_GRAMMAR.globals.symbol", None)
    ioc.provide('LL1_GRAMMAR.globals.list_direct', list())
    ioc.provide('LL1_GRAMMAR.globals.index', 0)
    ioc.provide('LL1_GRAMMAR.globals.stack', ['S'])


@pytest.fixture
def setup_parser():
    transitions = pd.read_csv('./data/processsed_lexer_table.csv', index_col=0)
    state_classes: Dict[
        Tuple[int, int, int, int], ApplyStrategyInterface
    ] = {
        (0, 0, 1, 0): ErrorNext(),
        (0, 1, 1, 0): ErrorStackNext(),
        (1, 0, 1, 0): AcceptErrorNext(),
        (0, 0, 0, 0): Next(),
        (0, 0, 1, 1): ErrorReturn(),
        (1, 0, 1, 1): AcceptErrorReturn(),
        (1, 0, 0, 0): AcceptNext(),
    }
    return transitions, state_classes


@pytest.mark.parametrize("row", [
    # """D""",
    "D()",
    """D(1,2)""",
    """D(D(1),k(true))""",
    "+(1, 2)",
    "!(1)",
    "1"
])
def test_bad_grammar(setup_parser, row):
    f = False
    try:
        initiation()
        current_state_idx = 1
        transitions, state_classes = setup_parser
        list_direct = get_follow_symbols_from_table(transitions, current_state_idx)
        ioc.override('LL1_GRAMMAR.globals.symbol', row)
        lexer = Lexer(list_direct, row)
        lexer.tokenize()
        ioc.override('LL1_GRAMMAR.globals.tokens', lexer.tokens)
        token_list = lexer.tokens
        ioc.override('LL1_GRAMMAR.globals.token', token_list[0])
        state_key = get_state_vector_from_table(
            transitions, current_state_idx
        )
        next_state_idx = get_next_idx_from_table(
            transitions, current_state_idx
        )
        initial_state = state_classes[state_key]
        current_state = initial_state
        ioc.override('LL1_GRAMMAR.globals.list_direct', lexer.list_direct)
        token = str(ioc.require("LL1_GRAMMAR.globals.token"))
        while True:
            current_state_idx = current_state(current_state_idx, next_state_idx)
            token = ioc.require("LL1_GRAMMAR.globals.token")
            if token == 'END' and current_state_idx == 'S':
                break
            current_symbols = get_follow_symbols_from_table(transitions, current_state_idx)
            ioc.override('LL1_GRAMMAR.globals.list_direct', current_symbols)
            state_key = get_state_vector_from_table(transitions, current_state_idx)
            next_state_idx = get_next_idx_from_table(transitions, current_state_idx)
            current_state = state_classes[state_key]
            token = str(ioc.require("LL1_GRAMMAR.globals.token"))
        token = ioc.require("LL1_GRAMMAR.globals.token")
        stack = ioc.require("LL1_GRAMMAR.globals.stack")
    except:
        f = True
    assert f