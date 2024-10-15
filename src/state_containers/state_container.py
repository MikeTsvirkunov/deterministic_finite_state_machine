from interfaces.state_container_interface import StateContainerInterface
from interfaces.state_interface import StateInterface


class StateContainer(StateContainerInterface):

    def __init__(self, container: dict[StateInterface, StateInterface]) -> None:
        self.__container__ = container 


    def __call__(self, state: StateInterface):
        return self.__container__[state]
