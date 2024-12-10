import json
import ioc
import pandas as pd
import pytest
import sys
sys.path.append(sys.path[0] + '\\..\\')
from src.ll1.states.StateA import StateA
from src.ll1.lexer import Lexer
from src.ll1.states.StateAER import StateAER
from src.ll1.states.StateNE import StateNE
from src.ll1.states.StateNE import StateNE
from src.ll1.states.StateNSE import StateNSE
from src.ll1.states.StateN import StateN
from src.ll1.states.StateNAE import StateNAE
from src.ll1.states.StateER import StateER
from src.ll1.states.StateAER import StateAER
from src.ll1.states.StateAR import StateAR
from  src.ll1.condition import Consts
from src.ll1.constants import TRANSITIONS


@pytest.fixture(autouse=True)
def reset_consts():
    Consts.TOKEN = None
    Consts.INDEX = 0
    Consts.STACK = []
    Lexer.tokens = []
    Lexer.list_direct = []
    Lexer.symbol = ''
    yield


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
    ioc.provide('LL1_GRAMMAR.globals.list_direct', list())
    ioc.provide('LL1_GRAMMAR.globals.index', 0)
    ioc.provide('LL1_GRAMMAR.globals.stack', ['S'])


@pytest.fixture
def setup_parser():
    transitions = pd.read_csv('./data/processsed_lexer_table.csv', index_col=0)
    state_classes = {
        (0, 0, 1, 0): StateNE, 
        (0, 1, 1, 0): StateNSE, 
        (1, 0, 1, 0): StateNAE, 
        (0, 0, 0, 0): StateN, 
        (0, 0, 1, 1): StateER,
        (1, 0, 1, 1): StateAER, 
        (1, 0, 0, 1): StateAR,
        (1, 0, 0, 0): StateA
    }
    return transitions, state_classes


@pytest.mark.parametrize("row", [
    # """D""",
    # "D()",
    # """D(1""",
    # """D(1,2)""",
    """D(D(1),2)""",
    # "+(1, 2)"
    # "!(1)"
    # "d(1 eps )"
    # "1"
    # "d"
])
def test_state_transition_positive(setup_parser, row):
    initiation()
    current_state_idx = 1
    transitions, state_classes = setup_parser
    list_direct = get_follow_symbols_from_table(transitions, current_state_idx)
    lexer = Lexer(list_direct, row)
    lexer.tokenize()
    token_list = lexer.get_tokens()
    Consts.TOKEN = token_list[0]
    state_key = get_state_vector_from_table(
        transitions, current_state_idx
    )
    next_state_idx = get_next_idx_from_table(
        transitions, current_state_idx
    )
    initial_state = state_classes[
        state_key
    ](
        current_state_idx, 
        next_state_idx,
        Consts.TOKEN
    )
    current_state = initial_state
    Consts.STACK.append('S')
    while Consts.TOKEN != 'END':
        current_state_idx = current_state.transition()
        if Consts.TOKEN == 'END' and current_state_idx == 'S':
            break
        current_symbols = get_follow_symbols_from_table(transitions, current_state_idx)
        ct = Consts.TOKEN
        ct2 = ioc.require('LL1_GRAMMAR.globals.token')
        Lexer(current_symbols, ct)
        state_key = get_state_vector_from_table(transitions, current_state_idx)
        next_state_idx = get_next_idx_from_table(transitions, current_state_idx)
        current_state = state_classes[state_key](current_state_idx, next_state_idx, Consts.TOKEN)
    assert len(Consts.STACK) == 0
    assert Consts.TOKEN == "END"
