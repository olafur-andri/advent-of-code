from dataclasses import dataclass
from typing import Any, Iterable, Sequence

@dataclass(frozen=True, eq=True)
class Seed:
    number: int

class Mapper:
    """Maps numbers from one level to the next"""
    
    @dataclass(frozen=True, eq=True)
    class Range:
        min: int
        max: int

        def __contains__(self, item: Any):
            if type(item) != int:
                return False
            return self.min <= item <= self.max

    @dataclass(frozen=True, eq=True)
    class Entry:
        source: "Mapper.Range"
        destination: "Mapper.Range"

    class SourceNotFoundError(ValueError):
        pass
    
    def __init__(self):
        self.__entries: list["Mapper.Entry"] = []

    def add_entry(self, destination_range_start: int, source_range_start: int, range_length: int):
        source_range = Mapper.Range(source_range_start, source_range_start + range_length - 1)
        destination_range = \
            Mapper.Range(destination_range_start, destination_range_start + range_length - 1)
        
        self.__entries.append(Mapper.Entry(source_range, destination_range))
    
    def map(self, number: int):
        for entry in self.__entries:
            if number in entry.source:
                shift = entry.destination.min - entry.source.min
                return number + shift
        
        return number

def get_seeds_from_input(filepath: str) -> list[Seed]:
    with open(filepath, "r") as input_file:
        first_line = next(input_file).strip()

    seed_numbers_str = first_line.replace("seeds: ", "")
    seed_numbers = map(int, seed_numbers_str.split())

    return [Seed(seed_number) for seed_number in seed_numbers]

def get_mapper_starting_at(start_index: int, lines: Sequence[str]):
    mapper = Mapper()
    current_index = start_index

    while current_index < len(lines) and lines[current_index].strip() != "":
        destination_range_start, source_range_start, range_length = \
            map(int, lines[current_index].split())
        mapper.add_entry(destination_range_start, source_range_start, range_length)

        current_index += 1
    
    return mapper

def get_mappers_from_input(filepath: str):
    mappers: list[Mapper] = []
    
    with open(filepath, "r") as input_file:
        lines = [line.strip() for line in input_file]

    for index, line in enumerate(lines):
        if "map:" in line:
            mappers.append(get_mapper_starting_at(index + 1, lines))
    
    return mappers

def get_location_number(seed: Seed, mappers: Iterable[Mapper]) -> int:
    current_number = seed.number

    for mapper in mappers:
        current_number = mapper.map(current_number)
    
    return current_number

def main():
    FILEPATH = "2023/day_5/input.txt"
    seeds = get_seeds_from_input(FILEPATH)
    mappers = get_mappers_from_input(FILEPATH)

    location_numbers = [get_location_number(seed, mappers) for seed in seeds]

    print(min(location_numbers))
    

if __name__ == "__main__":
    main()
