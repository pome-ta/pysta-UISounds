from pathlib import Path

import sound
import ui

root_str = '/System/Library/Audio/UISounds/'
root_path = Path(root_str)

all_files = list(root_path.glob('**/*.*'))
all_sounds = [sound.Player(str(s)) for s in all_files]
all_names = [
  f'{n: 04}: ' + str(name).replace(root_str, '').replace('/', ' - ')
  for n, name in enumerate(all_files)
]


class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.data_source = ui.ListDataSource(all_names)

    self.table_view = ui.TableView()
    self.table_view.data_source = self.data_source
    self.table_view.delegate = self
    self.table_view.flex = 'WH'

    self.add_subview(self.table_view)

  # xxx: ここで作るのもなぁ、、、
  def tableview_did_select(self, tableview, section, row):
    #print(all_files[row])
    all_sounds[row].play()


if __name__ == '__main__':
  view = View()
  view.present('fullscreen')

