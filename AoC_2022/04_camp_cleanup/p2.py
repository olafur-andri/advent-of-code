import sys

TRange = tuple[int, int]

def overlap(r1: TRange, r2: TRange):
  """Returns `True` iff `r1` overlaps with `r2`"""
  return (r1[0] >= r2[0] and r1[0] <= r2[1]) or \
         (r1[1] >= r2[0] and r1[1] <= r2[1])

def main():
  count = 0

  for line in sys.stdin:
    line = line.strip()
    r1_str, r2_str = line.split(",")
    r1 = tuple(map(int, r1_str.split("-")))
    r2 = tuple(map(int, r2_str.split("-")))
    count += int(overlap(r1, r2) or overlap(r2, r1))
  
  print(count)

if __name__ == "__main__":
  main()
