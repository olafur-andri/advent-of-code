def main():
  max_cal = float("-inf")
  curr_sum = 0
  with open("in.txt") as fs:
    for line in fs:
      line = line.strip()
      if line == "":
        max_cal = max(max_cal, curr_sum)
        curr_sum = 0
      else:
        curr_sum += int(line)
    
  print("max calories:", max_cal)

if __name__ == "__main__":
  main()