import math
from typing import Iterable
from DirectionLoop import DirectionLoop
from DesertMap import DesertMap

def product(numbers: Iterable[int]):
    result = 1

    for number in numbers:
        result *= number
    
    return result

def is_prime(number: int):
    if number < 2:
        return False

    limit = math.floor(math.sqrt(number))

    for i in range(2, limit + 1):
        if number % i == 0:
            return False
    
    return True

def all_prime_numbers():
    yield 2

    current_number = 3

    while True:
        if is_prime(current_number):
            yield current_number

        current_number += 2

def get_prime_factor_dict(number: int):
    prime_factor_dict: dict[int, int] = {}
    
    remainder = number

    while remainder > 1:
        for current_prime in all_prime_numbers():

            if remainder % current_prime == 0:
                remainder //= current_prime

                existing_frequency = prime_factor_dict.get(current_prime, 0)
                prime_factor_dict[current_prime] = existing_frequency + 1
                break
    
    return prime_factor_dict

def find_lowest_common_multiple(numbers: list[int]):
    prime_factor_dicts = [get_prime_factor_dict(number) for number in numbers]

    lcm_factor_dict: dict[int, int] = {}

    for prime_factor_dict in prime_factor_dicts:
        for prime_factor, new_frequency in prime_factor_dict.items():
            existing_frequency = lcm_factor_dict.get(prime_factor, 0)
            lcm_factor_dict[prime_factor] = max(existing_frequency, new_frequency)
    
    return product([prime_factor ** frequency for prime_factor, frequency in lcm_factor_dict.items()])

def is_target_node(node_name: str):
    return node_name[-1] == "Z"

def get_target_frequencies(desert_map: DesertMap, direction_loop: DirectionLoop):
    starting_nodes = [node for node in desert_map.get_all_nodes() if node[-1] == "A"]

    target_node_reached: list[bool] = [is_target_node(node) for node in starting_nodes]
    frequencies: list[int] = [0 for _ in starting_nodes]

    current_nodes = list(starting_nodes)

    desert_map.set_starting_nodes(starting_nodes)

    while not all(target_node_reached):
        current_nodes = desert_map.take_step_in(direction_loop.get_next_direction())
        
        for index, node in enumerate(current_nodes):
            if not target_node_reached[index]:
                frequencies[index] += 1
            
            if is_target_node(node):
                target_node_reached[index] = True            
    
    return frequencies

def main():
    FILEPATH = "AoC_2023/day_8/input.txt"

    direction_loop = DirectionLoop.from_file(FILEPATH)
    desert_map = DesertMap.from_file(FILEPATH)

    frequencies = get_target_frequencies(desert_map, direction_loop)

    print(find_lowest_common_multiple(frequencies))

    # ======================================

    # frequencies: list[int] = []

    # for i in range(786):
    #     direction_loop = DirectionLoop.from_file(FILEPATH)
    #     desert_map = DesertMap.from_file(FILEPATH)

    #     starting_node = desert_map.get_all_nodes()[i]

    #     if starting_node[-1] != "A":
    #         continue

    #     desert_map.set_starting_nodes([starting_node])

    #     current_node: str = starting_node
    #     nr_steps = 0
    #     nr_target_nodes = 0
    #     target_node_steps: list[int] = []
    #     NR_TARGET_NODES_LIMIT = 10

    #     while True:
    #         if current_node[-1] == "Z":
    #             target_node_steps.append(nr_steps)

    #             nr_target_nodes += 1

    #             if nr_target_nodes >= NR_TARGET_NODES_LIMIT:
    #                 break
            
    #         current_node = desert_map.take_step_in(direction_loop.get_next_direction())[0]

    #         nr_steps += 1

    #     print(f"Steps where we encountered a target node: {target_node_steps}")

    #     differences: list[int] = []

    #     for i in range(len(target_node_steps) - 1):
    #         differences.append(target_node_steps[i + 1] - target_node_steps[i])

    #     frequencies.append(differences[0])

    #     print(f"Differences:                              {differences}")
        
    #     print()

    # print(f"Frequencies: {frequencies}")
    # print(f"Lowest common multiple: {find_lowest_common_multiple(frequencies)}")

if __name__ == "__main__":
    main()
