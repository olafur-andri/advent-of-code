import sys

def get_score_dict():
  score: dict[str, int] = dict()
  curr_score = 1
  for i in range(ord("a"), ord("z")+1, 1):
    score[chr(i)] = curr_score
    curr_score += 1
  for i in range(ord("A"), ord("Z")+1, 1):
    score[chr(i)] = curr_score
    curr_score += 1
  return score

def main():
  score = get_score_dict()

  total = 0
  three_lines: list[str] = []
  for line in sys.stdin:
    line = line.strip()
    three_lines.append(line)

    if (len(three_lines) != 3):
      continue

    set1, set2, set3 = map(set, three_lines)
    intersection = set1.intersection(set2).intersection(set3)
    common_item = intersection.pop()
    total += score[common_item]
    three_lines.clear()
  
  print(total)

if __name__ == "__main__":
  main()