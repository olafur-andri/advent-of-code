from enum import Enum

class Direction(Enum):
    NORTH = 1
    WEST = 2
    SOUTH = 3
    EAST = 4

    @staticmethod
    def is_horizontal(direction: "Direction"):
        return direction in [Direction.WEST, Direction.EAST]
    
    @staticmethod
    def opposite(direction: "Direction"):
        if direction == Direction.NORTH:
            return Direction.SOUTH
        if direction == Direction.WEST:
            return Direction.EAST
        if direction == Direction.SOUTH:
            return Direction.NORTH
        if direction == Direction.EAST:
            return Direction.WEST
        
        raise ValueError(f"Don't know how to get the opposite of direction: '{direction}'")
