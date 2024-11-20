import ioc
from typing import Any, Collection
from binary_solvers import BinarySolverInterface
from dfsm.interfaces import (
    BranchStateInterface,
    RuleInterface, 
    StateInterface, 
    StateMapInterface
)


class OHSolver(StateMapInterface):

    def __init__(self, source_states_map: Collection[BranchStateInterface]):
        dublicate_rule: RuleInterface = ioc.require('Rules.StatesMap.ContainNoDublicates')
        validatror: BinarySolverInterface = ioc.require('Validators.StatesMap.ContainNoDublicates')
        r: bool = dublicate_rule(states_map=source_states_map)
        validatror(boolean=r)()
        self.__states_map__ = source_states_map


    @property
    def states_map(self):
        return self.__states_map__


    def next(self, branch_name: Any, state: StateInterface) -> StateInterface:
        for a in self.states_map:
            a_s = a.from_state
            if (state == a_s):
                return a.to_state
        return ioc.require('Constants.States.EmptyAction')