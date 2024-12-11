from enum import Enum, Flag


class Direction(int, Enum):
    up: int = 1
    down: int = -1
    stop: int = 0


class DoorsStates(Flag):
    opened: bool = True
    closed: bool = False


class ElevatorCommands(str, Enum):
    move_up: str = 'move up'
    move_down: str = 'move down'
    open_doors: str = 'open doors'
    close_doors: str = 'close doors'
