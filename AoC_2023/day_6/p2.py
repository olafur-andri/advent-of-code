from dataclasses import dataclass

@dataclass(frozen=True, eq=True)
class Race:
    duration: int
    record_distance: int

def get_race_from_input(filepath: str):
    with open(filepath, "r") as input_file:
        lines = [line.strip() for line in input_file.readlines()]
    
    first_line = lines[0]
    duration = int( first_line.replace("Time:", "").replace(" ", "") )

    second_line = lines[1]
    record_distance = int( second_line.replace("Distance:", "").replace(" ", "") )

    return Race(duration, record_distance)

def find_nr_ways_to_win(race: Race):
    nr_ways_to_win = 0

    for nr_hold_seconds in range(race.duration + 1):
        time_left = race.duration - nr_hold_seconds
        distance_traveled = nr_hold_seconds * time_left

        if distance_traveled > race.record_distance:
            nr_ways_to_win += 1
    
    return nr_ways_to_win

def product(numbers: list[int]):
    answer = 1

    for number in numbers:
        answer *= number

    return answer

def main():
    race = get_race_from_input("2023/day_6/input.txt")
    print( find_nr_ways_to_win(race) )

if __name__ == "__main__":
    main()
