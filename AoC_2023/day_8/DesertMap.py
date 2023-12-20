from dataclasses import dataclass
from Direction import Direction


class DesertMap:
    @dataclass(frozen=True, eq=True)
    class Pair:
        left: str
        right: str

        def to(self, direction: Direction):
            if direction == Direction.L:
                return self.left
            if direction == Direction.R:
                return self.right
            raise ValueError(f"Unrecognized direction: '{direction}'")

    def __init__(self):
        self.__node_dict: dict[str, DesertMap.Pair] = {}
        self.__current_nodes: list[str] = []
    
    @staticmethod
    def from_file(filepath: str):
        with open(filepath, "r") as input_file:
            desert_map = DesertMap()

            next(input_file)
            next(input_file)

            for line in input_file:
                current_node_name, lr_str = line.strip().split(" = ")
                left_node_name, right_node_name = lr_str.replace("(", "").replace(")", "").split(", ")
                desert_map.add_node(current_node_name, left_node_name, right_node_name)
            
            return desert_map

    def add_node(self, node_name: str, left_node_name: str, right_node_name: str):
        # if node_name in self.__node_dict:
        #     raise ValueError(f"Node with name '{node_name}' already exists in desert map")
        
        self.__node_dict[node_name] = DesertMap.Pair(left_node_name, right_node_name)
    
    def set_starting_nodes(self, starting_nodes: list[str]):
        # if len(self.__current_nodes) != 0:
        #     raise ValueError("Cannot set starting node when starting node has already been set")
        # if any(node not in self.__node_dict for node in starting_nodes):
        #     raise ValueError(f"Cannot find some starting node in this desert map")

        self.__current_nodes = starting_nodes

    def take_step_in(self, direction: Direction):
        # if len(self.__current_nodes) == 0:
        #     raise ValueError(f"Cannot take a step if starting node hasn't been set yet")
        # if any(node not in self.__node_dict for node in self.__current_nodes):
        #     raise ValueError(f"Could not find some node in this desert map")
        
        next_nodes = [self.__node_dict[node].to(direction) for node in self.__current_nodes]
        self.__current_nodes = next_nodes
        return next_nodes
    
    def get_current_nodes(self):
        return self.__current_nodes
    
    def get_all_nodes(self):
        return list( self.__node_dict.keys() )
