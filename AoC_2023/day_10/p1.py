from dataclasses import dataclass
from typing import Sequence
from types import MappingProxyType
from Direction import Direction

TCoord = tuple[int, int]
TPipeGrid = MappingProxyType[TCoord, str]

@dataclass(frozen=True, eq=True)
class DfsNode:
    coord: TCoord
    prev: "DfsNode | None"

def get_pipe_grid_from_input_file(filepath: str) -> tuple[TPipeGrid, int, int]:
    pipe_grid: dict[TCoord, str] = {}

    with open(filepath, "r") as input_file:
        lines = [line.strip() for line in input_file]
    
    nr_rows, nr_columns = len(lines), len(lines[0])

    for row in range(nr_rows):
        for column in range(nr_columns):
            pipe_grid[row, column] = lines[row][column]

    return MappingProxyType(pipe_grid), nr_rows, nr_columns

def find_starting_coord(pipe_grid: TPipeGrid, nr_rows: int, nr_columns: int) -> TCoord:
    for row in range(nr_rows):
        for column in range(nr_columns):
            if pipe_grid[row, column] == "S":
                return (row, column)
    
    raise ValueError("Could not find starting coordinate in the given pipe grid :(")

def step(coord: TCoord, direction: Direction):
        row, column = coord

        if direction == Direction.NORTH:
            return (row - 1, column)
        if direction == Direction.WEST:
            return (row, column - 1)
        if direction == direction.SOUTH:
            return (row + 1, column)
        if direction == direction.EAST:
            return (row, column + 1)
        
        raise ValueError(f"Don't know how to step in direction: '{direction}'")

def get_pipe_directions(pipe: str) -> tuple[Direction, ...]:
        if pipe == "|":
            return (Direction.NORTH, Direction.SOUTH)
        if pipe == "-":
            return (Direction.WEST, Direction.EAST)
        if pipe == "L":
            return (Direction.NORTH, Direction.EAST)
        if pipe == "J":
            return (Direction.NORTH, Direction.WEST)
        if pipe == "7":
            return (Direction.SOUTH, Direction.WEST)
        if pipe == "F":
            return (Direction.SOUTH ,Direction.EAST)
        if pipe == "S":
            return tuple(direction for direction in Direction)
        return ()

def coord_is_in_bounds(coord: TCoord, nr_rows: int, nr_columns: int):
    row, column = coord
    return (0 <= row < nr_rows) and (0 <= column < nr_columns)

def get_connected_neighbor_coords(coord: TCoord, pipe_grid: TPipeGrid, nr_rows: int, nr_columns: int) -> tuple[TCoord, ...]:
    connected_neighbor_coords: list[TCoord] = []

    my_pipe = pipe_grid[coord]
    my_pipe_directions = get_pipe_directions(my_pipe)

    for neighbor_direction in my_pipe_directions:
        neighbor_coord = step(coord, neighbor_direction)

        if not coord_is_in_bounds(neighbor_coord, nr_rows, nr_columns):
            continue

        neighbor_pipe = pipe_grid[neighbor_coord]
        neighbor_pipe_directions = get_pipe_directions(neighbor_pipe)
        neighbor_is_connected = Direction.opposite(neighbor_direction) in neighbor_pipe_directions

        if neighbor_is_connected:
            connected_neighbor_coords.append(neighbor_coord)

    return tuple(connected_neighbor_coords)

def derive_loop_from_target_dfs_node(target_dfs_node: DfsNode):
    starting_coord = target_dfs_node.coord
    loop: list[TCoord] = []

    loop.append(starting_coord)

    current_dfs_node = target_dfs_node.prev

    while current_dfs_node != None and current_dfs_node.coord != starting_coord:
        loop.append(current_dfs_node.coord)
        current_dfs_node = current_dfs_node.prev

    return tuple(loop)

def get_main_loop(pipe_grid: TPipeGrid, nr_rows: int, nr_columns: int) -> tuple[TCoord, ...]:
    starting_coord = find_starting_coord(pipe_grid, nr_rows, nr_columns)
    dfs_node_stack: list[DfsNode] = []
    target_dfs_node: DfsNode | None = None;

    dfs_node_stack.append(DfsNode(starting_coord, None))

    while len(dfs_node_stack) > 0:
        current_dfs_node = dfs_node_stack.pop()
        current_coord = current_dfs_node.coord
        prev_coord = None if current_dfs_node.prev == None else current_dfs_node.prev.coord

        neighbor_coords = get_connected_neighbor_coords(current_coord, pipe_grid, nr_rows, nr_columns)

        for neighbor_coord in neighbor_coords:
            if neighbor_coord == prev_coord:
                continue

            new_dfs_node = DfsNode(coord=neighbor_coord, prev=current_dfs_node)
            is_target_dfs_node = neighbor_coord == starting_coord

            if is_target_dfs_node:
                target_dfs_node = new_dfs_node
                break
            
            dfs_node_stack.append(new_dfs_node)
    
    assert target_dfs_node != None

    return derive_loop_from_target_dfs_node(target_dfs_node)

def get_nr_steps_to_farthest_point(loop: Sequence[TCoord]) -> int:
    loop_size = len(loop)
    return loop_size // 2

def main():
    INPUT_FILEPATH = "AoC_2023/day_10/input.txt"

    pipe_grid, nr_rows, nr_columns = get_pipe_grid_from_input_file(INPUT_FILEPATH)
    main_loop = get_main_loop(pipe_grid, nr_rows, nr_columns)
    distance_to_farthest_point = get_nr_steps_to_farthest_point(main_loop)

    print(distance_to_farthest_point)

if __name__ == "__main__":
    main()
