import sys

def main():
  lines = sys.stdin.readlines()
  lines = [l.strip() for l in lines]
  xs: list[int] = [1, 1] # xs[i] denotes the value of register X during the i-th cycle

  # build `xs`
  for line in lines:
    tokens = line.split()
    instr_name = tokens[0]
    xs.append(xs[-1])
    if instr_name == "addx":
      amount = int(tokens[1])
      xs.append(xs[-1] + amount)
  
  NR_ROWS = 6
  NR_COLS = 40
  curr_cycle = 1
  for _ in range(NR_ROWS):
    for col in range(NR_COLS):
      sprite_pos = xs[curr_cycle]
      pixel_pos = col
      if abs(pixel_pos - sprite_pos) <= 1:
        print("#", end="")
      else:
        print(".", end="")
      curr_cycle += 1
    print()

if __name__ ==  "__main__":
  main()
