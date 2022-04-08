from pathlib import Path
import ui
import sound

root = Path('/System/Library/Audio/UISounds')

modern = 'Modern'
nano = 'nano'
new = 'New'

root_path = root  # / new


class Pad(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'slategray'
    self.note = None

  def touch_began(self, touch):
    self.bg_color = 'maroon'
    self.note.play()

  def touch_ended(self, touch):
    self.bg_color = 'slategray'
    #self.note.stop()


class WrapGrid(ui.View):
  def __init__(self, g_size, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.height = g_size
    self.width = g_size
    self.border_width = 1
    self.border_color = 1
    self.set_pads()

  def set_pads(self):
    self.pad = Pad()
    self.pad.width = self.width * .8
    self.pad.height = self.height * .8
    self.pad.corner_radius = 8
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
    file_path = root_path.iterdir()
    sound_list = [file for file in file_path if not file.is_dir()]
    _x, _y, _w, _h = self.frame
    set_size = min(_w, _h) * 0.25
    count = 0
    pad_line = 4
    for n, x in enumerate(range(64)):
      wrap = WrapGrid(set_size)
      set_y = int(-(-n / pad_line))
      if n % 4 == 0:
        set_x = 0
      wrap.x = set_size * set_x
      wrap.y = set_size * set_y
      num = ui.Label()
      num.text = str(count)
      set_x += 1
      count += 1
      wrap.pad.note = sound.Player(str(sound_list[n]))
      wrap.pad.add_subview(num)
      #self.scroll_view.add_subview(wrap)
      self.add_subview(wrap)


class MainView(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'red'
    self.rack = RackGrid()
    self.rack.flex = 'WH'
    self.add_subview(self.rack)


if __name__ == '__main__':
  view = MainView()
  view.present('fullscreen')

