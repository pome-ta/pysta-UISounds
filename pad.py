from pathlib import Path
import ui
import sound

root_str = '/System/Library/Audio/UISounds/'
root = Path(root_str)

modern = 'Modern'
nano = 'nano'
new = 'New'

root_path = root  #/ new  # todo: `/path` で追加

#@ui.in_background
def get_sounds(call_root_path):
  # xxx: とりあえず、直下ファイル取得
  file_path = call_root_path.iterdir()
  sound_list = [file for file in file_path if not file.is_dir()]
  print(len(sound_list))

get_sounds(root_path)


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

  def layout(self):
    #self.height = self.superview.height * 0.88
    #self.width = self.superview.width * 0.88
    #self.center = self.superview.center
    self.name_label.size_to_fit()

  def touch_began(self, touch):
    self.bg_color = self.active_color
    self.note.play()

  def touch_ended(self, touch):
    def animation():
      self.bg_color = self.default_color

    ui.animate(animation, duration=0.2)


class WrapGrid(ui.View):
  def __init__(self, g_size, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.height = g_size
    self.width = g_size
    self.border_width = 0.5
    self.border_color = 0.5
    self.set_pad()

  def set_pad(self):
    self.pad = Pad()
    self.pad.width = self.width * .88
    self.pad.height = self.height * .88
    self.pad.center = self.center
    self.add_subview(self.pad)
    


class RackGrid(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'steelblue'
    self.scroll_view = ui.ScrollView()
    self.scroll_view.flex = 'WH'
    #self.add_subview(self.scroll_view)
    self.set_pads()

  @ui.in_background
  def set_pads(self):
    print('rack')
    file_path = root_path.iterdir()
    sound_list = [file for file in file_path if not file.is_dir()]
    _x, _y, _w, _h = self.frame
    set_size = min(_w, _h) * 0.25
    count = 0
    pad_line = 4
    for n, file in enumerate(sound_list):
      wrap = WrapGrid(set_size)
      set_y = int(-(-n / pad_line))
      if n % 4 == 0:
        set_x = 0
      wrap.x = set_size * set_x
      wrap.y = set_size * set_y

      name = str(file).replace(root_str, '')
      wrap.pad.name_label.text = f'\n{count}: \n{name}'
      wrap.pad.note = sound.Player(str(file))
      self.add_subview(wrap)
      #self.scroll_view.add_subview(wrap)

      set_x += 1
      count += 1


class MainView(ui.View):
  def __init__(self, *args, **kwargs):
    print('init')
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'red'
    self.rack = RackGrid()
    self.rack.flex = 'WH'
    self.add_subview(self.rack)

  def layout(self):
    print('lay')
    #pass


if __name__ == '__main__':
  view = MainView()
  view.present('fullscreen')

