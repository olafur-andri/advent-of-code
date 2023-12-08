import sys

def get_matrix(lines: list[str]):
  matrix: list[list[int]] = []
  for line in lines:
    line = line.strip()
    matrix.append(list(map(int, line)))
  return matrix

def get_scenic_score(matrix: list[list[int]], row: int, col: int):
  my_height = matrix[row][col]

  # try to go north
  score_north = 0
  curr_row = row-1
  while curr_row >= 0:
    score_north += 1
    if matrix[curr_row][col] >= my_height:
      break
    curr_row -= 1
  
  # try to go west
  score_west = 0
  curr_col = col-1
  while curr_col >= 0:
    score_west += 1
    if matrix[row][curr_col] >= my_height:
      break
    curr_col -= 1
  
  # try to go south
  score_south = 0
  curr_row = row+1
  while curr_row < len(matrix):
    score_south += 1
    if matrix[curr_row][col] >= my_height:
      break
    curr_row += 1
  
  # try to go east
  score_east = 0
  curr_col = col+1
  while curr_col < len(matrix[0]):
    score_east += 1
    if matrix[row][curr_col] >= my_height:
      break
    curr_col += 1
  
  return score_north * score_west * score_south * score_east

def get_max_scenic_score(matrix: list[list[int]]):
  max_score = 0
  for row in range(0, len(matrix)):
    for col in range(0, len(matrix[0])):
      curr_score = get_scenic_score(matrix, row, col)
      max_score = max(max_score, curr_score)
  return max_score

def main():
  lines = sys.stdin.readlines()
  matrix = get_matrix(lines)
  max_score = get_max_scenic_score(matrix)
  print(max_score)

if __name__ == "__main__":
  main()