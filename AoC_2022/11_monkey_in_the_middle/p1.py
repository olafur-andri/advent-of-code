import sys
from collections import deque

class Monkey:
  items: deque[int] # the items this monkey is currently holding
  count: int # how many times this monkey inspected an item
  __op = lambda old: old # maps an old worry level to a new worry level
  __test = lambda wl: 0 # maps a worry level to the monkey ID that should receive this item

  def __init__(self, items: list[int], op, test):
    self.items = deque(items)
    self.__op = op
    self.__test = test
    self.count = 0
  
  def perform_op(self, old: int):
    return self.__op(old)

  def perform_test(self, wl: int):
    return self.__test(wl)



def parse_op_str(op_str: str):
  return lambda old: eval(op_str)

def get_test_lambda(divisible_by: int, if_true_id: int, if_false_id: int):
  return lambda wl: if_true_id if (wl % divisible_by == 0) else if_false_id

def get_monkeys(lines: list[str]):
  monkeys: list[Monkey] = []
  
  for i in range(1, len(lines), 7):
    items = list( map(int, lines[i][16::].split(", ")) )

    op = parse_op_str(lines[i+1][17::])

    divisible_by = int(lines[i+2][19::])
    if_true_id = int(lines[i+3][25::])
    if_false_id = int(lines[i+4][26::])
    # test = lambda wl: if_true_id if (wl % divisible_by == 0) else if_false_id
    test = get_test_lambda(divisible_by, if_true_id, if_false_id)

    new_monkey = Monkey(items, op, test)
    monkeys.append(new_monkey)

  return monkeys

def perform_round(monkeys: list[Monkey]):
  for monkey in monkeys:
    while len(monkey.items) > 0:
      monkey.count += 1
      wl = monkey.items.popleft()
      wl = monkey.perform_op(wl)
      wl //= 3
      new_id = monkey.perform_test(wl)
      monkeys[new_id].items.append(wl)

def main():
  lines = sys.stdin.readlines()
  lines = [l.strip() for l in lines]
  monkeys = get_monkeys(lines)
  
  for _ in range(20):
    perform_round(monkeys)
  
  counts: list[int] = []
  for i in range(len(monkeys)):
    print(f"Monkey {i} inspected items {monkeys[i].count} times.")
    counts.append(monkeys[i].count)
  print()

  counts.sort(reverse=True)
  print(f"monkey business: {counts[0] * counts[1]}")


if __name__ == "__main__":
  main()