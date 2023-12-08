from dataclasses import dataclass
from typing import Any, Iterable, Sequence

@dataclass(frozen=True, eq=True)
class Range:
    start: int
    length: int

    def is_empty(self):
        return self.length <= 0

    def min(self):
        if self.is_empty():
            raise ValueError("Cannot get min of an empty range")
        
        return self.start

    def max(self):
        if self.is_empty():
            raise ValueError("Cannot get max of an empty range")
        
        return self.start + self.length - 1

    def intersection(self, other_range: "Range"):
        new_start = max(self.start, other_range.start)
        new_end = min(self.max(), other_range.max())
        new_length = max(0, new_end - new_start + 1)
        
        return Range(new_start, new_length)
    
    def shift(self, shift: int):
        return Range(self.start + shift, self.length)

    def remove(self, other_range: "Range") -> list["Range"]:
        if self in other_range:
            return []
        
        if other_range in self:
            left_range = Range(self.min(), other_range.min() - self.min())

            right_range_start = other_range.max() + 1
            right_range = Range(right_range_start, self.max() - right_range_start + 1)

            new_ranges: list[Range] = []    
            if not left_range.is_empty():
                new_ranges.append(left_range)
            if not right_range.is_empty():
                new_ranges.append(right_range)
            
            return new_ranges
        
        return self.remove(self.intersection(other_range))

    def __contains__(self, item: Any):
        if type(item) not in (int, Range):
            return False
        
        if type(item) == int:
            return self.min() <= item <= self.max()
        
        return self.min() <= item.min() and self.max() >= item.max()

class Mapper:
    """Maps numbers from one level to the next"""

    @dataclass(frozen=True, eq=True)
    class Entry:
        source_range: Range
        destination_range: Range

    class SourceNotFoundError(ValueError):
        pass
    
    def __init__(self):
        self.__entries: list["Mapper.Entry"] = []

    def add_entry(self, destination_range_start: int, source_range_start: int, range_length: int):
        source_range = Range(source_range_start, range_length)
        destination_range = Range(destination_range_start, range_length)
        
        self.__entries.append(Mapper.Entry(source_range, destination_range))
    
    def map_range(self, unmapped_range: Range):
        unmapped_ranges = set([unmapped_range])
        mapped_ranges: list[Range] = []

        for mapper_entry in self.__entries:
            # have to copy to prevent mutation of set while iterating over it
            unmapped_ranges_copy = list(unmapped_ranges)

            for unmapped_range in unmapped_ranges_copy:
                entry_intersection = unmapped_range.intersection(mapper_entry.source_range)

                if entry_intersection.is_empty():
                    continue

                shift = mapper_entry.destination_range.min() - mapper_entry.source_range.min()
                mapped_range = entry_intersection.shift(shift)
                mapped_ranges.append(mapped_range)

                old_unmapped_range = unmapped_range
                unmapped_ranges.remove(old_unmapped_range)

                new_unmapped_ranges = old_unmapped_range.remove(entry_intersection)
                unmapped_ranges.update(new_unmapped_ranges)
        
        mapped_ranges.extend(unmapped_ranges)

        return mapped_ranges

def get_seed_number_ranges_from_input(filepath: str):
    seed_ranges: list[Range] = []

    with open(filepath, "r") as input_file:
        first_line = next(input_file).strip()

    seed_tokens_str = first_line.replace("seeds: ", "")
    seed_tokens = tuple( map(int, seed_tokens_str.split()) )

    for i in range(0, len(seed_tokens), 2):
        range_start = seed_tokens[i]
        range_length = seed_tokens[i + 1]
        seed_ranges.append(Range(range_start, range_length))

    return seed_ranges

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

def map_to_location_number_ranges(seed_range: Range, mappers: Iterable[Mapper]):
    current_ranges: tuple[Range, ...] = (seed_range,)

    for mapper in mappers:
        new_ranges: list[Range] = []

        for current_range in current_ranges:
            new_ranges.extend(mapper.map_range(current_range))
        
        current_ranges = tuple(new_ranges)
    
    return current_ranges

def get_lowest_location_number(seed_number_ranges: Iterable[Range], mappers: Iterable[Mapper]):
    lowest_location_number = float("inf")

    for seed_number_range in seed_number_ranges:
        location_number_ranges = map_to_location_number_ranges(seed_number_range, mappers) 
        current_lowest_location_number = min([r.min() for r in location_number_ranges])
        lowest_location_number = min(lowest_location_number, current_lowest_location_number)
    
    return lowest_location_number

def main():
    FILEPATH = "2023/day_5/input.txt"
    seed_number_ranges = get_seed_number_ranges_from_input(FILEPATH)
    mappers = get_mappers_from_input(FILEPATH)
    lowest_location_number = get_lowest_location_number(seed_number_ranges, mappers)

    print(lowest_location_number)
    

if __name__ == "__main__":
    main()
