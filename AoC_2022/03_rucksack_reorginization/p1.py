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
  for line in sys.stdin:
    line = line.strip()
    l = len(line) // 2
    l_half_set = set(line[0:l])
    r_half_str = line[l::]
    for c in r_half_str:
      if c in l_half_set:
        total += score[c]
        break
  
  print(total)

if __name__ == "__main__":
  main()