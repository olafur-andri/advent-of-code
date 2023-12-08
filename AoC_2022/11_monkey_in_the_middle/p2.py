from __future__ import annotations
import sys
from collections import deque
from typing import Union

class Divisibility:
  """A class that holds 'divisiblity' information for a number, namely, "what is
     this number modulo x" where x is in some predefined and small set.

     Let "i" denote the number this class represents and "x" represent the
     factor to check for whether "i" is divisible by "x"
  """
  __factors: list[int] = [] # maps an "x" to ("i" mod "x"). if __modulos[x] == 0, then "i" is divisible by "x"

  @staticmethod
  def set_factors(factors: list[int]):
    """Lets every `Divisiblity` instances know which factors we want to look out
       for, i.e., what are our "x's"
    """
    Divisibility.__factors = factors
  
  def __init__(self, initial_value: Union[int, dict[int, int]]):
    self.__modulos = dict()
    if type(initial_value) == int:
      for factor in Divisibility.__factors:
        self.__modulos[factor] = initial_value % factor
    else: # type(initial_value) == dict
      self.__modulos.update(initial_value)
  
  def __add__(self, other: int):
    new_modulos = self.__modulos.copy()
    for factor in new_modulos:
      new_modulos[factor] = (new_modulos[factor] + other) % factor
    return Divisibility(new_modulos)
  
  def __mul__(self, other: int | Divisibility):
    new_modulos = self.__modulos.copy()
    if type(other) == int:
      for factor in new_modulos:
        new_modulos[factor] = (new_modulos[factor] * other) % factor
    else: # type(other) == Divisiblity
      for factor in new_modulos:
        new_modulos[factor] = (new_modulos[factor] * other.__modulos[factor]) % factor
    return Divisibility(new_modulos)

  def is_divisible_by(self, factor: int):
    return self.__modulos[factor] == 0


class Monkey:
  def __init__(self, items: list[Divisibility], op, test):
    self.items = deque(items)
    self.__op = op
    self.__test = test
    self.count = 0
  
  def perform_op(self, old: Divisibility):
    return self.__op(old)

  def perform_test(self, wl: Divisibility):
    return self.__test(wl)



def parse_op_str(op_str: str):
  return lambda old: eval(op_str)

def get_test_lambda(divisible_by: int, if_true_id: int, if_false_id: int):
  return lambda wl: if_true_id if wl.is_divisible_by(divisible_by) else if_false_id

def get_monkeys(lines: list[str]):
  monkeys: list[Monkey] = []
  
  for i in range(1, len(lines), 7):
    items_ints = list( map(int, lines[i][16::].split(", ")) )
    items = [Divisibility(i) for i in items_ints]

    op = parse_op_str(lines[i+1][17::])

    divisible_by = int(lines[i+2][19::])
    if_true_id = int(lines[i+3][25::])
    if_false_id = int(lines[i+4][26::])
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
      new_id = monkey.perform_test(wl)
      monkeys[new_id].items.append(wl)

def get_factors(lines: list[str]):
  factors: list[int] = []
  for i in range(3, len(lines), 7):
    factor = int(lines[i][19::])
    factors.append(factor)
  return factors

def main():
  lines = sys.stdin.readlines()
  lines = [l.strip() for l in lines]

  # find the factors and use them to initialize `Divisibility`, this has to
  # happen before Monkey instances are gathered
  factors = get_factors(lines)
  Divisibility.set_factors(factors)

  # get Monkey instances
  monkeys = get_monkeys(lines)
  


  # TOO SLOW
  for _ in range(10_000):
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