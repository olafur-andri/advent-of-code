def main():
  sums: list[int] = []
  curr_sum = 0

  with open("in.txt") as fs:
    for line in fs:
      line = line.strip()
      if line == "":
        sums.append(curr_sum)
        curr_sum = 0
      else:
        curr_sum += int(line)
  
  sums.sort(reverse=True)
  print("top three calories:", sums[0] + sums[1] + sums[2])

if __name__ == "__main__":
  main()