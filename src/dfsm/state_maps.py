import ioc
from typing import Any, Callable, Collection
from src.binary_solvers import BinarySolverInterface
from src.dfsm.interfaces import (
    BranchStateInterface,
    RuleInterface, 
    StateInterface, 
    StateMapInterface,
    ExtendableInterface
)


class DefaultStateMap(StateMapInterface):

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
            an = a.name
            if (an == branch_name) and (state == a.from_state):
                return a.to_state
        return next(iter(filter(
            lambda a: (a.name == branch_name) and (a.from_state == state), 
            self.states_map
        ))).to_state


class ExtendableStateMap(StateMapInterface, ExtendableInterface):

    def __init__(self, source_states_map: Collection[BranchStateInterface]):
        validatror: BinarySolverInterface = ioc.require('Validators.DublicatesValidator')
        validatror(state_map=source_states_map)()
        self.__states_map__ = source_states_map


    @property
    def states_map(self):
        return self.__states_map__


    def next(self, branch_name: Any, state: StateInterface) -> StateInterface:
        return next(iter(filter(
            lambda a: (a.name == branch_name) and (a.from_state == state), 
            self.states_map
        ))).to_state


    def extend(self, value: Any):
        adding_uniq_rule: RuleInterface = ioc.require('Rules.StatesMap.AddingUniqBranch')
        validatror: BinarySolverInterface = ioc.require('Validators.StatesMap.AddingUniqBranch')
        r: bool = adding_uniq_rule(states_map=self.__states_map__, new_branch=value)
        validatror(boolean=r)()
        self.__states_map__.append(value)
