# [Pythonista-Issues/sysinfo.py at master · omz/Pythonista-Issues · GitHub](https://github.com/omz/Pythonista-Issues/blob/master/scripts/sysinfo.py)

# wip: コード整理する

import plistlib
import sys
import platform
from pathlib import Path
from objc_util import ObjCClass, on_main_thread
import clipboard


def get_pythonista_version_info():
  version = None
  bundle_version = None

  try:
    plist = plistlib.loads(
      (Path(sys.executable).parent / 'Info.plist').read_bytes())
    version = plist['CFBundleShortVersionString']
    bundle_version = plist['CFBundleVersion']

  except Exception:
    pass

  return 'Pythonista {} ({})'.format(version or 'N/A', bundle_version or 'N/A')


def get_python_interpreter_info():
  return 'Default interpreter {}.{}.{}'.format(*sys.version_info)


def get_device_info():
  device = ObjCClass('UIDevice').currentDevice()
  main_screen = ObjCClass('UIScreen').mainScreen()
  native_size = main_screen.nativeBounds().size

  return 'iOS {}, model {}, resolution (portrait) {} x {} @ {}'.format(
    device.systemVersion(), platform.machine(), native_size.width,
    native_size.height, main_screen.nativeScale())


def outSoundLog():
  root_str = '/System/Library/Audio/UISounds/'
  root_path = Path(root_str)

  all_files = list(root_path.glob('**/*.*'))
  print('```')
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
  print('```')


@on_main_thread  # clipboard.set or freeze
def main():
  separator = '--- SYSTEM INFORMATION ---'

  info = '\n'.join([
    '**System Information**',
    '',
    '* {}, {}'.format(get_pythonista_version_info(),
                      get_python_interpreter_info()),
    '* {}'.format(get_device_info()),
  ])
  print('# pysta-UISounds')
  print('')
  print('```')
  print('\n'.join([separator, info]))
  print('```')
  print('')
  print('サウンド一覧')
  print('')
  outSoundLog()
  '''
  print(
    'Please, attach everything between {} to your GitHub issue, many thanks.'.
    format(separator))
  clipboard.set(info)
  print(
    'System information was just stored in the system clipboard. You can paste it with Cmd V.'
  )
  '''


if __name__ == '__main__':
  main()

