import sys

def get_matrix(lines: list[str]):
  matrix: list[list[int]] = []
  for line in lines:
    line = line.strip()
    matrix.append(list(map(int, line)))
  return matrix

def is_visible(matrix: list[list[int]], row: int, col: int):
  my_height = matrix[row][col]

  # try to go north
  vis_north = True
  for curr_row in range(row-1, -1, -1):
    if matrix[curr_row][col] >= my_height:
      vis_north = False
      break
  
  # try to go west
  vis_west = True
  for curr_col in range(col-1, -1, -1):
    if matrix[row][curr_col] >= my_height:
      vis_west = False
      break
  
  # try to go south
  vis_south = True
  for curr_row in range(row+1, len(matrix)):
    if matrix[curr_row][col] >= my_height:
      vis_south = False
      break
  
  # try to go east
  vis_east = True
  for curr_col in range(col+1, len(matrix[0])):
    if matrix[row][curr_col] >= my_height:
      vis_east = False
      break
  
  return vis_north or vis_west or vis_south or vis_east

def count_visible(matrix: list[list[int]]):
  count = 0
  for row in range(0, len(matrix)):
    for col in range(0, len(matrix[0])):
      if is_visible(matrix, row, col):
        count += 1
  return count

def main():
  lines = sys.stdin.readlines()
  matrix = get_matrix(lines)
  count = count_visible(matrix)
  print(count)

if __name__ == "__main__":
  main()