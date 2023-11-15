import sys

X = 0
Y = 1
TCoord = tuple[int, int]
TInstr = tuple[str, int]

def get_instructions(lines: list[str]):
  instructions: list[TInstr] = []
  for line in lines:
    line = line.strip()
    dir_str, dist_str = line.split()
    instructions.append((dir_str, int(dist_str)))
  return instructions

def move_head(head_pos: TCoord, dir_str: str):
  x, y = head_pos
  if dir_str == "R":
    return (x+1, y)
  if dir_str == "U":
    return (x, y+1)
  if dir_str == "D":
    return (x, y-1)
  if dir_str == "L":
    return (x-1, y)
  raise Exception("BROKEN :(")

def minus(c1: TCoord, c2: TCoord):
  return (c1[X] - c2[X], c1[Y] - c2[Y])

def plus(c1: TCoord, c2: TCoord):
  return (c1[X] + c2[X], c1[Y] + c2[Y])

def move_tail(tail_pos: TCoord, head_pos: TCoord):
  # get the vector from tail to head
  delta = minus(head_pos, tail_pos)

  # if head is adjacent, don't move tail
  if abs(delta[X]) <= 1 and abs(delta[Y]) <= 1:
    return tail_pos

  # normalize the vector such that it only contains 1's or -1's or 0's
  norm_delta = (
    delta[X] // abs(delta[X]) if delta[X] != 0 else delta[X],
    delta[Y] // abs(delta[Y]) if delta[Y] != 0 else delta[Y],
  )

  # move the tail in any direction that contains a 1 or -1 from `delta`
  new_tail_pos = plus(tail_pos, norm_delta)
  
  return new_tail_pos

def print_board(rows: int, cols: int, head_pos: TCoord, tail_pos: TCoord):
  for y in range(rows-1, -1, -1):
    for x in range(cols):
      char = "H" if head_pos == (x,y) else "T" if tail_pos == (x,y) else "."
      print(char, end="")
    print()
  print("\n")

def main():
  head_pos: TCoord = (0, 0)
  tail_pos: TCoord = (0, 0)
  tail_coords: set[TCoord] = set([tail_pos])

  lines = sys.stdin.readlines()
  instructions = get_instructions(lines)

  # print_board(rows=5, cols=6, head_pos=head_pos, tail_pos=tail_pos)
  for dir_str, dist in instructions:
    for _ in range(dist):
      head_pos = move_head(head_pos, dir_str)
      tail_pos = move_tail(tail_pos, head_pos)
      tail_coords.add(tail_pos)
      # print_board(rows=5, cols=6, head_pos=head_pos, tail_pos=tail_pos)

  print(len(tail_coords))

if __name__ == "__main__":
  main()