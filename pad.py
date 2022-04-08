from pathlib import Path
import sound
import ui

GRID_ROW = 4


#@ui.in_background
def get_items(items):
  file_path = items.iterdir()
  return [file for file in file_path if not file.is_dir()]


class Pad(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.default_color = 'slategray'
    self.active_color = 'maroon'
    self.bg_color = self.default_color
    self.corner_radius = 8

    self.name_label = ui.Label()
    self.name_label.number_of_lines = 0
    self.name_label.font = ('Source Code Pro', 8)
    self.name_label.flex = 'WH'
    self.add_subview(self.name_label)

    self.note = None

  def set_up(self, file_path):
    path = f'{file_path}'
    self.name_label.text = path
    self.note = sound.Player(path)

  def touch_began(self, touch):
    self.bg_color = self.active_color
    self.note.play()

  def touch_ended(self, touch):
    '''
    def animation():
      self.bg_color = self.default_color
    ui.animate(animation, duration=0.2)
    '''
    self.bg_color = self.default_color


class WrapGrid(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.border_width = 0.8
    self.border_color = 0.8
    self.pad = Pad()
    self.add_subview(self.pad)

  def set_pad(self, file_path):
    self.pad.set_up(file_path)

  def layout(self):
    self.pad.height = self.height * 0.88
    self.pad.width = self.width * 0.88
    self.pad.center = self.center


class RackGrid(ui.View):
  #@ui.in_background
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'slategray'
    self.flex = 'WH'

    self.scroll_view = ui.ScrollView()
    #self.scroll_view.bounces = 0
    #self.scroll_view.scroll_enabled = 0
    self.scroll_view.bg_color = 'steelblue'
    self.scroll_view.flex = 'WH'
    self.add_subview(self.scroll_view)
    #self.set_grid(items)

  @ui.in_background
  def set_grid(self, item_list):
    # xxx: 引数を持たせると`ui.in_background` ダメ？
    items = get_items(item_list)
    for item in items:
      grid = WrapGrid()
      grid.set_pad(item)
      self.scroll_view.add_subview(grid)
    # xxx: 同期
    self.layout()

  def layout(self):
    _, _, w, h = self.frame
    set_size = min(w, h) / GRID_ROW
    height_mult = int(-(-len(self.scroll_view.subviews) // GRID_ROW))

    self.scroll_view.content_size = (self.width, set_size * height_mult)

    for n, sub_view in enumerate(self.scroll_view.subviews):
      set_x = 0 if n % 4 == 0 else set_x
      set_y = int(-(-n / GRID_ROW))
      sub_view.height = sub_view.width = set_size
      sub_view.x = set_size * set_x
      sub_view.y = set_size * set_y
      set_x += 1

  def touch_began(self, touch):
    print(self.scroll_view.dragging)


class RootView(ui.View):
  def __init__(self, items, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'maroon'
    self.rack = RackGrid()
    self.rack.set_grid(items)
    self.add_subview(self.rack)

  def layout(self):
    #print(f'layout_root: {self.frame}')
    pass


if __name__ == '__main__':
  root_str = '/System/Library/Audio/UISounds/'
  root_path = Path(root_str)

  root = RootView(root_path)

  #root.present(style='fullscreen', orientations=['portrait'])
  root.present(style='fullscreen')

