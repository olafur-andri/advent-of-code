from enum import Enum
from dataclasses import dataclass
from types import MappingProxyType
from typing import Iterable

class NumberDerivationError(ValueError):
    pass

class Direction(Enum):
    NORTH = 1
    NORTHWEST = 2
    WEST = 3
    SOUTHWEST = 4
    SOUTH = 5
    SOUTHEAST = 6
    EAST = 7
    NORTHEAST = 8

@dataclass(eq=True, frozen=True)
class Coordinate:
    """Represents a (row, column) coordinate"""
    row: int
    column: int

    def step(self, direction: Direction):
        if direction == Direction.NORTH:
            return Coordinate(self.row - 1, self.column)
        if direction == Direction.NORTHWEST:
            return Coordinate(self.row - 1, self.column - 1)
        if direction == Direction.WEST:
            return Coordinate(self.row, self.column - 1)
        if direction == Direction.SOUTHWEST:
            return Coordinate(self.row + 1, self.column - 1)
        if direction == Direction.SOUTH:
            return Coordinate(self.row + 1, self.column)
        if direction == Direction.SOUTHEAST:
            return Coordinate(self.row + 1, self.column + 1)
        if direction == Direction.EAST:
            return Coordinate(self.row, self.column + 1)
        if direction == Direction.NORTHEAST:
            return Coordinate(self.row - 1, self.column + 1)
        
        raise ValueError(f"Don't know how to step in direction: {direction}")

@dataclass
class Number:
    """Represents *any* number in an engine, not necessarily a part number"""
    row: int
    start_column: int
    end_column: int
    value: int

    def get_nr_digits(self):
        return self.end_column - self.start_column
    
    def get_left_coordinate(self):
        return Coordinate(self.row, self.start_column)

    def get_right_coordinate(self):
        return Coordinate(self.row, self.end_column)
    
    def get_all_coordinates(self):
        columns = range(self.start_column, self.end_column + 1)
        return [Coordinate(self.row, column) for column in columns]

    def has_coordinate(self, coordinate: Coordinate):
        if coordinate.row != self.row:
            return False
        
        return self.start_column <= coordinate.column <= self.end_column

@dataclass
class Gear:
    """Represents a gear in the engine"""
    part_number_1: Number
    part_number_2: Number

class Engine:
    def __init__(
        self,
        nr_rows: int,
        nr_columns: int,
        grid_dict: MappingProxyType[Coordinate, str]
    ):
        self.__nr_rows = nr_rows
        self.__nr_columns = nr_columns
        self.__grid_dict = grid_dict
    
    def __str__(self):
        output = ""

        for row in range(self.get_nr_rows()):
            for column in range(self.get_nr_columns()):
                output += self.__grid_dict[Coordinate(row, column)]

            output += "\n"
        
        return output
    
    def get_nr_rows(self):
        return self.__nr_rows
    
    def get_nr_columns(self):
        return self.__nr_columns

    def char_at(self, coordinate: Coordinate):
        return self.__grid_dict[coordinate]
    
    def is_within_bounds(self, coordinate: Coordinate):
        row_is_within_bounds = 0 <= coordinate.row < self.get_nr_rows()
        column_is_within_bounds = 0 <= coordinate.column < self.get_nr_columns()
        return row_is_within_bounds and column_is_within_bounds


def parse_engine_from_input_file(filepath: str):
    engine_dict: dict[Coordinate, str] = {}
    nr_rows, nr_columns = 0, 0
    
    with open(filepath, "r") as input_file:
        lines = [l.strip() for l in input_file.readlines() if not l.isspace()]

        nr_rows = len(lines)
        nr_columns = len(lines[0])

        for row, line in enumerate(lines):
            line = line.strip()

            for column, character in enumerate(line):
                engine_dict[Coordinate(row, column)] = character

    return Engine(nr_rows, nr_columns, MappingProxyType(engine_dict))

def derive_number_starting_at(engine: Engine, starting_coordinate: Coordinate):
    number_str = ""
    current_coordinate = starting_coordinate
    end_column = starting_coordinate.column

    while engine.is_within_bounds(current_coordinate) and engine.char_at(current_coordinate).isdigit():
        number_str += engine.char_at(current_coordinate)
        end_column = current_coordinate.column
        current_coordinate = current_coordinate.step(Direction.EAST)
    
    if number_str == "":
        raise NumberDerivationError(f"Could not find a number at starting coordinate: {starting_coordinate}")
    
    return Number(starting_coordinate.row, starting_coordinate.column, end_column, int(number_str))

def find_all_numbers_in_engine(engine: Engine):
    numbers: list[Number] = []
    nr_rows, nr_columns = engine.get_nr_rows(), engine.get_nr_columns()

    for row in range(nr_rows):
        column = 0

        while column < nr_columns:
            try:
                number = derive_number_starting_at(engine, Coordinate(row, column))
                numbers.append(number)
                column += number.get_nr_digits()
            except NumberDerivationError:
                pass

            column += 1
    
    return numbers

def get_neighboring_coordinates(engine: Engine, number: Number):
    all_possible_coordinates: list[Coordinate] = []
    left_coordinate, right_coordinate = number.get_left_coordinate(), number.get_right_coordinate()
    number_coordinates = number.get_all_coordinates()

    # corners
    all_possible_coordinates.extend([
        left_coordinate.step(Direction.NORTHWEST),
        left_coordinate.step(Direction.SOUTHWEST),
        right_coordinate.step(Direction.NORTHEAST),
        right_coordinate.step(Direction.SOUTHEAST),
    ])

    # sides
    all_possible_coordinates.extend([
        left_coordinate.step(Direction.WEST),
        right_coordinate.step(Direction.EAST),
    ])

    # upper
    all_possible_coordinates.extend(c.step(Direction.NORTH) for c in number_coordinates)

    # lower
    all_possible_coordinates.extend(c.step(Direction.SOUTH) for c in number_coordinates)

    return [c for c in all_possible_coordinates if engine.is_within_bounds(c)]

def is_symbol(character: str):
    assert len(character) == 1
    return (not character.isdigit()) and (character != ".")

def is_part_number(engine: Engine, number: Number):
    neighboring_coordinates = get_neighboring_coordinates(engine, number)
    return any([is_symbol( engine.char_at(coordinate) ) for coordinate in neighboring_coordinates])

def find_all_part_numbers(engine: Engine, numbers: Iterable[Number]):
    return [number for number in numbers if is_part_number(engine, number)]

def number_is_adjacent(coordinate: Coordinate, number: Number):
    return any([number.has_coordinate(coordinate.step(direction)) for direction in Direction])

def get_adjacent_numbers(coordinate: Coordinate, part_numbers: Iterable[Number]):
    return [part_number for part_number in part_numbers if number_is_adjacent(coordinate, part_number)]

def find_gears(engine: Engine, part_numbers: Iterable[Number]):
    gears: list[Gear] = []

    nr_rows, nr_columns = engine.get_nr_rows(), engine.get_nr_columns()
    possible_gear_coordinates = [Coordinate(r, c) for r in range(nr_rows) for c in range(nr_columns) \
                                 if engine.char_at(Coordinate(r, c)) == "*"]
    
    for possible_gear_coordinate in possible_gear_coordinates:
        adjacent_part_numbers = get_adjacent_numbers(possible_gear_coordinate, part_numbers)
        
        if len(adjacent_part_numbers) != 2:
            continue

        gears.append(Gear(adjacent_part_numbers[0], adjacent_part_numbers[1]))
    
    return gears

def main():
    engine = parse_engine_from_input_file("input.txt")
    numbers = find_all_numbers_in_engine(engine)
    part_numbers = find_all_part_numbers(engine, numbers)

    gears = find_gears(engine, part_numbers)

    print(sum([ gear.part_number_1.value * gear.part_number_2.value for gear in gears ]))

if __name__ == "__main__":
    main()
