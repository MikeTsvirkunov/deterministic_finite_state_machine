from unittest.mock import Mock
import pandas as pd

from ll1.applying_strategies import AcceptErrorNext, AcceptErrorReturn, AcceptNext, ErrorNext, ErrorReturn, ErrorStackNext, Next
from ll1.interfaces import ApplyStrategyHavingInterface, CurrentStateId, NextStateId
from src.dfsm.interfaces import StateInterface


state_classes = {
    (0, 0, 1, 0): ErrorNext, 
    (0, 1, 1, 0): ErrorStackNext, 
    (1, 0, 1, 0): AcceptErrorNext, 
    (0, 0, 0, 0): Next, 
    (0, 0, 1, 1): ErrorReturn,
    (1, 0, 1, 1): AcceptErrorReturn,
    (1, 0, 0, 0): AcceptNext
}


def get_ll_state_from_pandas_row(row: pd.Series) -> StateInterface:
    
    current_idx = row['FROM'].item()
    next_idx = row['NEXT'].item()
    symbols = row['FOLLOW_SYMBOLS'].item()
    key = row.loc['NEXT','ACCEPT','STACK','ERROR','RETURN'].values.tolist()

    x = Mock(
        spec=StateInterface | ApplyStrategyHavingInterface | NextStateId | CurrentStateId | 
    )
    x.__hash__ = lambda s: 