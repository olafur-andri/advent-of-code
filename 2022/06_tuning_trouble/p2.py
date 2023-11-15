def main():
  line = input()
  for i in range(14, len(line)):
    chars = line[i-14:i]
    if len(set(chars)) == len(chars):
      print(i)
      return

if __name__ == "__main__":
  main()