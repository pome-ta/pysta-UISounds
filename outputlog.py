from pathlib import Path
from pprint import pprint

root_str = '/System/Library/Audio/UISounds/'
root_path = Path(root_str)

all_files = list(root_path.glob('**/*.*'))


pre_outlog = ''
for dir_file in all_files:
  addr_list = str(dir_file).replace(root_str, '').split('/')
  for i, addr in enumerate(addr_list):
    if i == 0:
      if pre_outlog != addr:
        print(addr)
      pre_outlog = addr
    else:
      print('  ', addr)

