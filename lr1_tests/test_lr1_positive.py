import ioc
import pandas as pd
import pytest
import sys
sys.path.append(sys.path[0] + '\\..\\')
from src.lr1.lr_actions import ExecutingCodes, error_acccept_action, get_state_vector, lr1_parcer_initiation, parse_row, provide_grammar, provide_input_string, r_action, s_action, step_initiation, success_acccept_action

state_map_table = {
    (1, 0, 0, 0): error_acccept_action,
    (0, 1, 0, 0): s_action,
    (0, 0, 1, 0): r_action,
    (0, 0, 0, 1): success_acccept_action
}

@pytest.fixture
def get_grammar():
    table = pd.read_csv('data/gramma_table_lr1.csv', index_col=0).T.to_dict()
    with open('data/grammar_rules') as f:
        grammar_rules = f.read()
    grammar_rules = list(map(lambda a: (a.split(' ::= ')[0], a.split(' ::= ')[1].split(' ')), grammar_rules.split('\n')))
    return table, grammar_rules


@pytest.mark.parametrize("row", [
    "D()",
    """D(1,2)""",
    """D(D(1),k(true))""",
    "+(1, 2)",
    "!(1)",
    "1"
])
def test(get_grammar, row):
    table, grammar_rules = get_grammar
    lr1_parcer_initiation()
    provide_grammar(grammar_rules, table)
    input_string = parse_row(row)
    d = {
        'SEPARATOR': ',',
        'LPAR': '(',
        'RPAR': ')',
        'SUM': '+',
        'MUT': '*',
        'REMUT': '/',
        'DELTA': '-',
        'AND': '&',
        'OR': '|',
        'NOT': '!',
        'LARGER': '>',
        'BIGGER': '<',
        'BEQUAL': '='
    }
    input_string_processed = list(map(lambda a: d[a] if a in d else a, input_string))
    provide_input_string(input_string_processed)
    flag = ioc.require('LR1.globals.is_success')
    while flag == ExecutingCodes.none:
        step_initiation()
        state_vector = get_state_vector()
        strategy = state_map_table.get(state_vector, error_acccept_action)
        strategy()
        flag = ioc.require('LR1.globals.is_success')
    assert flag == ExecutingCodes.success_code

