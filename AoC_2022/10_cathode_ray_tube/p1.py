import sys

def main():
  lines = sys.stdin.readlines()
  lines = [l.strip() for l in lines]
  xs: list[int] = [1, 1] # xs[i] denotes the value of register X during the i-th cycle

  for line in lines:
    tokens = line.split()
    instr_name = tokens[0]
    xs.append(xs[-1])
    if instr_name == "addx":
      amount = int(tokens[1])
      xs.append(xs[-1] + amount)
  
  total_strength = 0
  for i in range(20, 221, 40):
    curr_strength = i * xs[i]
    print(f"signal strenght during {i}th cycle: {curr_strength}")
    total_strength += curr_strength
  print(f"\ntotal signal strength: {total_strength}")

if __name__ ==  "__main__":
  main()
