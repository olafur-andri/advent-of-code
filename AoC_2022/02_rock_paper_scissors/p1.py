import sys
from enum import Enum

class Move(Enum):
  ROCK = 0
  PAPER = 1
  SCISSORS = 2

class Result(Enum):
  WIN = 0
  DRAW = 1
  LOSS = 2

def do_i_win(my_move: Move, their_move: Move):
  if (my_move, their_move) == (Move.ROCK, Move.SCISSORS) or \
     (my_move, their_move) == (Move.SCISSORS, Move.PAPER) or \
     (my_move, their_move) == (Move.PAPER, Move.ROCK):
    return Result.WIN
  if my_move == their_move:
    return Result.DRAW
  return Result.LOSS

def parse_move(move_str: str):
  if move_str in ("A", "X"):
    return Move.ROCK
  if move_str in ("B", "Y"):
    return Move.PAPER
  if move_str in ("C", "Z"):
    return Move.SCISSORS

def move_to_points(move: Move):
  if move == Move.ROCK:
    return 1
  if move == Move.PAPER:
    return 2
  if move == Move.SCISSORS:
    return 3

def result_to_point(result: Result):
  if result == Result.LOSS:
    return 0
  if result == Result.DRAW:
    return 3
  if result == Result.WIN:
    return 6

def main():
  total = 0

  for line in sys.stdin:
    line = line.strip()
    their_move_str, my_move_str = line.split()
    their_move = parse_move(their_move_str)
    my_move = parse_move(my_move_str)
    result = do_i_win(my_move, their_move)
    total += move_to_points(my_move) + result_to_point(result)
  
  print(total)

if __name__ == "__main__":
  main()