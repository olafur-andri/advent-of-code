import sys
from enum import IntEnum

class Move(IntEnum):
  ROCK     = 1
  PAPER    = 2
  SCISSORS = 3

class Result(IntEnum):
  LOSS = 0
  DRAW = 3
  WIN  = 6

str_to_move = { "A": Move.ROCK, "B": Move.PAPER, "C": Move.SCISSORS }
what_wins_against = {
  Move.ROCK: Move.PAPER,
  Move.PAPER: Move.SCISSORS,
  Move.SCISSORS: Move.ROCK,
}
what_loses_against = {
  Move.PAPER: Move.ROCK,
  Move.SCISSORS: Move.PAPER,
  Move.ROCK: Move.SCISSORS,
}

def get_my_move(their_move: Move, desired_result: Result):
  if desired_result == Result.DRAW:
    return their_move
  if desired_result == Result.WIN:
    return what_wins_against[their_move]
  return what_loses_against[their_move]

def parse_result(result_str: str):
  if result_str == "X":
    return Result.LOSS
  if result_str == "Y":
    return Result.DRAW
  if result_str == "Z":
    return Result.WIN

def main():
  total = 0

  for line in sys.stdin:
    line = line.strip()
    their_move_str, result_str = line.split()
    their_move = str_to_move[their_move_str]
    desired_result = parse_result(result_str)
    my_move = get_my_move(their_move, desired_result)
    total += int(my_move) + int(desired_result)
  
  print(total)

if __name__ == "__main__":
  main()