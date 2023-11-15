import sys
from collections import deque

TStack = deque[str]
TInstr = tuple[int, int, int]

def get_stacks(lines: list[str]):
  # figure out how many stacks we'll need
  for line in lines:
    if not line.startswith(" 1"):
      continue
    l = int(line.split()[-1])
    break
  
  # initialize the stacks
  stacks: list[TStack] = [deque() for _ in range(l)]

  # read in the state of each stack
  for line in lines:
    if line.startswith(" 1"): # reached stack labels
      break
    i = 0
    c = 0
    while c < len(line):
      crate_label = line[c+1]
      if crate_label.strip() != "":
        stacks[i].appendleft(crate_label)
      i += 1
      c += 4

  return stacks

def get_instructions(lines: list[str]):
  instructions: list[TInstr] = []

  for line in lines:
    if not line.startswith("move"):
      continue
    l = line.replace("move ", "").replace("from ", "").replace("to ", "")
    a, b, c = map(int, l.split())
    instructions.append((a, b, c))
  
  return instructions

def apply_instruction(instruction: TInstr, stacks: list[TStack]):
  m, f, t = instruction
  moved_crates: list[str] = []
  for _ in range(m, 0, -1):
    moved_crates.append(stacks[f-1].pop())
  moved_crates.reverse()
  stacks[t-1].extend(moved_crates)

def main():
  # read in lines as list of strings
  lines = sys.stdin.readlines()

  # read in the starting state of the stacks
  stacks = get_stacks(lines)

  # read in the movement instructions
  instructions = get_instructions(lines)

  # apply the instructions in-place
  for instruction in instructions:
    apply_instruction(instruction, stacks)
  
  # read the top crates
  top_crate_labels = ""
  for stack in stacks:
    top_crate_labels += stack[-1]

  print(top_crate_labels)

if __name__ == "__main__":
  main()
