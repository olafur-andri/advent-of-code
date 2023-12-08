from enum import Enum
from types import MappingProxyType
from typing import Iterable, Sequence

class ColorParseError(ValueError):
    pass

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

class Observation:
    def __init__(self, color_count_dict: MappingProxyType[Color, int]):
        self.__color_count_dict = self.__construct_complete_color_count_dict(color_count_dict)
    
    def get_nr_of(self, color: Color):
        return self.__color_count_dict[color]
    
    def __construct_complete_color_count_dict(self, color_count_dict: MappingProxyType[Color, int]):
        """Returns a "complete" color count dict, i.e., a dict that is guaranteed to contain a key
           for each possible color value
        """
        return MappingProxyType( { color: color_count_dict.get(color, 0) for color in Color } )

class Game:
    def __init__(self, id: int, observations: Sequence[Observation]):
        self.__id = id
        self.__observations = observations
    
    def get_id(self):
        return self.__id

    def get_observation(self, observation_index: int):
        return self.__observations[observation_index]
    
    def get_nr_of_observations(self):
        return len(self.__observations)

def parse_game_id_from_line(line: str):
    words = line.split()
    return int( words[1].replace(":", "") )

def parse_color_from_obs_token(observation_token: str):
    _, color_name = observation_token.split()

    if color_name == "red":
        return Color.RED
    if color_name == "green":
        return Color.GREEN
    if color_name == "blue":
        return Color.BLUE
    
    raise ColorParseError(f"Don't know how to parse color from following obs. token: '{observation_token}'")

def parse_count_from_obs_token(observation_token: str):
    return int( observation_token.split()[0] )

def parse_color_count_dict_from_obs_str(observation_string: str):
    color_count_dict: dict[Color, int] = {}

    tokens = observation_string.split(", ")

    for token in tokens:
        color = parse_color_from_obs_token(token)
        count = parse_count_from_obs_token(token)
        color_count_dict[color] = count

    return MappingProxyType(color_count_dict)

def parse_observations_from_line(line: str):
    observations: list[Observation] = []

    _, observations_csv_string = line.split(": ")

    for observation_string in observations_csv_string.split("; "):
        color_count_dict = parse_color_count_dict_from_obs_str(observation_string)
        observations.append(Observation(color_count_dict))
    
    return observations

def parse_game_from_line(line: str):
    game_id = parse_game_id_from_line(line)
    observations = parse_observations_from_line(line)
    return Game(game_id, observations)

def parse_games_from_input_file():
    with open("input.txt", "r") as input_file:
        return [parse_game_from_line(line.strip()) for line in input_file]

def color_count_is_possible(color: Color, count: int):
    if color == Color.RED:
        return 0 <= count <= 12
    if color == Color.GREEN:
        return 0 <= count <= 13
    if color == Color.BLUE:
        return 0 <= count <= 14
    return count == 0

def observation_is_possible(observation: Observation):
    return all([ color_count_is_possible(color, observation.get_nr_of(color)) for color in Color ])

def game_is_possible(game: Game):
    for observation_index in range(game.get_nr_of_observations()):
        observation = game.get_observation(observation_index)

        if not observation_is_possible(observation):
            return False

    return True

def collect_possible_games_out_of(all_games: Iterable[Game]):
    return [game for game in all_games if game_is_possible(game)] 

def main():
    all_games = parse_games_from_input_file()
    possible_games = collect_possible_games_out_of(all_games)
    print(sum(game.get_id() for game in possible_games))

if __name__ == "__main__":
    main()
