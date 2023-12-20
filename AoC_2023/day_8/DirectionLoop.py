from Direction import Direction


class DirectionLoop:
    def __init__(self, direction_loop_str: str):
        self.__direction_loop = self.__get_direction_loop_from_str(direction_loop_str)
        self.__direction_index = 0
    
    @staticmethod
    def from_file(filepath: str):
        with open(filepath, "r") as input_file:
            first_line = input_file.readline().strip()
        
        return DirectionLoop(first_line)

    def get_next_direction(self):
        next_direction = self.__direction_loop[self.__direction_index]

        self.__direction_index = (self.__direction_index + 1) % len(self.__direction_loop)

        return next_direction
    
    def get_offset(self):
        return self.__direction_index
    
    @staticmethod
    def __get_direction_loop_from_str(direction_loop_str: str):
        loop_list: list[Direction] = []

        for letter in direction_loop_str:
            if letter == "R":
                loop_list.append(Direction.R)
            elif letter == "L":
                loop_list.append(Direction.L)
            else:
                raise ValueError(f"Unrecognized direction letter '{letter}'")
        
        return tuple(loop_list)