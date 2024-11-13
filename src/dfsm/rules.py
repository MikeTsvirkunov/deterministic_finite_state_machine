from typing import Collection
from dfsm.interfaces import BranchStateInterface, RuleInterface


class StateMapContainNoDublicates(RuleInterface):

    def __call__(self, *args, **kwargs):
        states_map: Collection[BranchStateInterface] = kwargs['states_map']
        # return all([branch_i != branch_j for i, branch_i in enumerate(states_map[:-1]) for branch_j in states_map[i+1:]])
        for i, branch_i in enumerate(states_map[:-1]):
            for branch_j in states_map[i+1:]:
                a, b = branch_i.__hash__(), branch_j.__hash__()
                if branch_i == branch_j:
                    return False
        return True


class AddingUniqBranch(RuleInterface):

    def __call__(self, *args, **kwargs):
        states_map: Collection[BranchStateInterface] = kwargs['states_map']
        new_branch: BranchStateInterface = kwargs['new_branch']
        return new_branch in states_map
