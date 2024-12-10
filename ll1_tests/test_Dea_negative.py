# import pytest
# import sys
# sys.path.append(sys.path[0] + '\\..\\')
# from lexer.lexer import Lexer
# from states.StateNE import StateNE
# from states.StateNE import StateNE
# from states.StateNSE import StateNSE
# from states.StateN import StateN
# from states.StateNAE import StateNAE
# from states.StateER import StateER
# from states.StateAER import StateAER
# from states.StateAR import StateAR
# from consts import Consts

# @pytest.fixture(autouse=True)
# def reset_consts():
#     Consts.TOKEN = None
#     Consts.INDEX = 0
#     Consts.STACK = []
#     Lexer.tokens = []
#     Lexer.list_direct = []
#     Lexer.symbol = ''
#     yield
# @pytest.fixture
# def setup_parser():
#     transitions = Consts.TRANSITIONS
#     state_classes = [StateNE, StateNSE, StateNAE, StateN, StateER, StateAER, StateAR]
#     return transitions, state_classes
# @pytest.mark.parametrize("row", [
#     "(2+)",
#     "2 >",
#     """
#     def func_sus(a)
#         return a + 2
#     """
# ])
# def test_state_transition_positive(setup_parser, row):
#     with pytest.raises(SyntaxError):
#         transitions, state_classes = setup_parser
#         lexer = Lexer(transitions[1][0], row)
#         lexer.tokenize()
#         token_list = lexer.get_tokens()
#         Consts.TOKEN = token_list[0]
#         initial_state = state_classes[transitions[1][-1]](1, transitions[1][1], Consts.TOKEN)
#         current_state = initial_state
#         while Consts.TOKEN != 'END':
#             current_state = current_state.transition()
#             Lexer(transitions[current_state][0],Consts.TOKEN)
#             current_state = state_classes[transitions[current_state][-1]](current_state, transitions[current_state][1], Consts.TOKEN)

# @pytest.mark.parametrize("row2", [
#     "1+#"
# ])
# def test_state_transition_no_tokens(setup_parser, row2):
#     with pytest.raises(ValueError):
#         transitions, state_classes = setup_parser
#         lexer = Lexer(transitions[1][0], row2)
#         lexer.tokenize()