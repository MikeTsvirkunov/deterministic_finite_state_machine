import ioc
from src.actions import empty_action, throw_exception
from src.binary_solvers import DefaultBinarySolver
from src.dfsm.rules import AddingUniqBranch, StateMapContainNoDublicates


def rules_providing():
    ioc.provide('Rules.StatesMap.ContainNoDublicates', StateMapContainNoDublicates())
    ioc.provide('Rules.StatesMap.AddingUniqBranch', AddingUniqBranch)
    


def validators_providing():
    ioc.provide('Validators.StatesMap.ContainNoDublicates', DefaultBinarySolver(
        binary_actions_map={
            True: empty_action,
            False: lambda: throw_exception(AttributeError, 'Setting state_map with dublicates.')
        }
    ))
    ioc.provide('Validators.StatesMap.AddingUniqBranch', DefaultBinarySolver(
        binary_actions_map={
            True: empty_action(),
            False: lambda: throw_exception(AttributeError, 'Adding dublicated value to state_map')
        }
    ))
