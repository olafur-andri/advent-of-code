from DesertMap import DesertMap
from DirectionLoop import DirectionLoop

def get_nr_steps_to_reach_destination(desert_map: DesertMap, direction_loop: DirectionLoop):
    TARGET_NODE = "ZZZ"

    desert_map.set_starting_nodes(["AAA"])

    nr_steps = 0

    while desert_map.get_current_nodes()[0] != TARGET_NODE:
        desert_map.take_step_in(direction_loop.get_next_direction())
        nr_steps += 1
    
    return nr_steps

def main():
    FILEPATH = "AoC_2023/day_8/input.txt"
    direction_loop = DirectionLoop.from_file(FILEPATH)
    desert_map = DesertMap.from_file(FILEPATH)
    nr_steps = get_nr_steps_to_reach_destination(desert_map, direction_loop)
    
    print(nr_steps)

if __name__ == "__main__":
    main()
