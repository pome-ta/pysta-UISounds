from pathlib import Path
import sound
import ui

GRID_ROW = 4


def get_sound_paths(paths):
  #file_path = paths.iterdir()
  #return [file for file in file_path if not file.is_dir()]
  return list(paths.glob('**/*.*'))


class Pad(ui.View):

  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.default_color = 'lightsteelblue'
    self.active_color = 'maroon'
    self.bg_color = self.default_color
    self.corner_radius = 8

    self.note = None

    self.name_label = ui.Label()
    self.name_label.number_of_lines = 0
    self.name_label.font = ('Source Code Pro', 10)
    self.name_label.flex = 'WH'
    self.add_subview(self.name_label)

  def set_up(self, file_path, parent_index):
    note_path = f'{file_path}'
    directly_list = note_path.split('/')
    note_name_list = directly_list[parent_index:]
    self.name_label.text = '/'.join(note_name_list)
    self.note = note_path

  @ui.in_background
  def touch_began(self, touch):
    sound.play_effect(self.note)
    self.bg_color = self.active_color

    def animation():
      self.bg_color = self.default_color

    ui.animate(animation, duration=1.0)


class WrapGrid(ui.View):

  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.border_width = 0.8
    self.border_color = 0.8
    self.pad = Pad()
    self.add_subview(self.pad)

  def set_pad(self, file_path, origin_index):
    self.pad.set_up(file_path, origin_index)

  def layout(self):
    self.pad.height = self.height * 0.88
    self.pad.width = self.width * 0.88
    self.pad.x = (self.height / 2) - (self.pad.height / 2)
    self.pad.y = (self.width / 2) - (self.pad.width / 2)


class RackGrid(ui.View):

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

  @ui.in_background
  def set_grid(self, origin_path):
    sound_path_list = get_sound_paths(origin_path)
    origin_index = len(f'{origin_path}'.split('/'))
    for s_path in sound_path_list:
      grid = WrapGrid()
      grid.alpha = 0.0
      grid.set_pad(s_path, origin_index)
      self.scroll_view.add_subview(grid)
    # xxx: 同期
    self.layout()

  def layout(self):
    _, _, w, h = self.frame
    set_size = min(w, h) / GRID_ROW
    height_mult = int(-(-len(self.scroll_view.subviews) // GRID_ROW))

    self.scroll_view.content_size = (self.width, set_size * height_mult)

    for n, sub_view in enumerate(self.scroll_view.subviews):

      def animation():
        sub_view.alpha = 1.0

      ui.animate(animation, duration=0.2)

      set_x = 0 if n % 4 == 0 else set_x
      set_y = int(-(-n / GRID_ROW))
      sub_view.height = sub_view.width = set_size
      sub_view.x = set_size * set_x
      sub_view.y = set_size * set_y

      set_x += 1


class RootView(ui.View):

  def __init__(self, sound_path, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'maroon'
    self.rack = RackGrid()
    self.rack.set_grid(sound_path)
    self.add_subview(self.rack)

    self.all_stop_btn = self.create_btn('iob:stop_32')
    self.all_stop_btn.action = (lambda sender: sound.stop_all_effects())
    self.right_button_items = [self.all_stop_btn]

  def create_btn(self, icon):
    btn_icon = ui.Image.named(icon)
    return ui.ButtonItem(image=btn_icon)


if __name__ == '__main__':
  root_str = '/System/Library/Audio/UISounds/'
  root_path = Path(root_str)
  root_view = RootView(root_path)

  #root_view.present(style='fullscreen', orientations=['portrait'])
  root_view.present(style='fullscreen')

