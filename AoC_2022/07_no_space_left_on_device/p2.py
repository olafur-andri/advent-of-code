from __future__ import annotations
import sys

class File:
  size = 0
  name = ""
  def __init__(self, size: int, name: str):
    self.size = size
    self.name = name

class Directory:
  files: list[File] = []
  dirs: list[Directory] = []
  name: str = ""
  parent_dir: Directory = None
  def __init__(
    self,
    name: str = "",
    parent_dir: Directory|None = None,
    files: list[File] = None,
    dirs: list[Directory] = None
  ):
    self.name = name
    self.parent_dir = parent_dir
    self.files = files if files != None else []
    self.dirs = dirs if dirs != None else []
  
  def get_subdir(self, subdir_name: str):
    """Returns the immediate subdirectory with the given name (NOTE: this method
       assumes that there exists such a subdirectory)
    """
    # making the assumption that a subdirectory will be listed before it's
    # navigated to
    for d in self.dirs:
      if d.name == subdir_name:
        return d
    raise ValueError(f"No subdirectory with name '{subdir_name}' found")

  def get_size(self):
    """Returns the total size of this directory"""
    total_size = 0
    for d in self.dirs:
      total_size += d.get_size()
    for f in self.files:
      total_size += f.size
    return total_size
  
  def am_root(self):
    return self.name == "/"



def build_file_system_tree(lines: list[str]):
  """Returns the file system tree according to the given input lines"""
  root = Directory(name="/")
  curr_dir = root
  for line in lines:
    line = line.strip()
    if line.startswith("$ "):
      line = line.replace("$ ", "")
      if line.startswith("cd"): # `cd` handling
        new_folder_name = line.replace("cd ", "")
        if new_folder_name == "/":
          curr_dir = root
        elif new_folder_name == "..":
          curr_dir = curr_dir.parent_dir
        else:
          curr_dir = curr_dir.get_subdir(new_folder_name)
      # can ignore `ls` commands
    elif line.startswith("dir"): # listing a directory
      dir_name = line.replace("dir ", "")
      new_dir = Directory(name=dir_name, parent_dir=curr_dir)
      curr_dir.dirs.append(new_dir)
    else: # listing a file
      split_line = line.split(" ")
      file_size = int(split_line[0])
      file_name = " ".join(split_line[1::])
      new_file = File(file_size, file_name)
      curr_dir.files.append(new_file)
  return root

def get_dirs_where(root: Directory, cond):
  """Start at the given root and collect all Directory instances that satisfy
     the given condition lambda
  """
  dirs: list[Directory] = []
  if cond(root):
    dirs.append(root)
  for subdir in root.dirs:
    dirs += get_dirs_where(subdir, cond)
  return dirs

def print_file_system(root: Directory, level=0):
  print("\t"*level + f"- {root.name} (dir)")
  for f in root.files:
    print("\t"*(level+1) + f"- {f.name} (file, size={f.size})")
  for d in root.dirs:
    print_file_system(d, level+1)

def main():
  MAX_SPACE = 70_000_000
  UPDATE_SIZE = 30_000_000

  lines = sys.stdin.readlines()
  root = build_file_system_tree(lines)
  
  # print("-- DEBUG --")
  # print_file_system(root)
  # print("\n\n")

  space_available = MAX_SPACE - root.get_size()
  req_dir_size = UPDATE_SIZE - space_available
  dirs = get_dirs_where(
    root,
    lambda d: d.get_size() >= req_dir_size
  )
  
  min_dir_size = float("inf")
  for d in dirs:
    min_dir_size = min(min_dir_size, d.get_size())
  
  print(min_dir_size)


if __name__ == "__main__":
  main()