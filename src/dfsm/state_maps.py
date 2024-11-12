from typing import Any, Collection
from dfsm.interfaces import BranchStateInterface, StateInterface, StateMapInterface


class DefaultStateMap(StateMapInterface):

    def __init__(self, source_states_map: Collection[BranchStateInterface]):
        assert len(source_states_map) == len(set(source_states_map)), 'Have been gotted state map with dublicated branches.'
        self.__states_map__ = source_states_map
    

    @property
    def states_map(self):
        return self.__states_map__


    def next(self, branch_name: Any, state: StateInterface) -> StateInterface:
        return next(iter(filter(
            lambda a: (a.name == branch_name) and (a.from_state == state), 
            self.states_map
        ))).to_state
