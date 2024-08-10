#!/usr/bin/env python

import os
import sys
import subprocess
import platform
import urllib.request
import stat

# We assume shell.py will assign SCRIPT_PARENT_DIR
SCRIPT_PARENT_DIR = os.environ.get('SCRIPT_PARENT_DIR', os.path.dirname(__file__))
SPD = SCRIPT_PARENT_DIR

DRAWIO_VERSION = '24.7.5'
DRAWIO_EXE_UNK_SYS_URL = f'https://github.com/jgraph/drawio-desktop/releases/download/v{DRAWIO_VERSION}/draw.io-{DRAWIO_VERSION}-windows-no-installer.exe'
DRAWIO_EXE_URL = {
  'linux':    f'https://github.com/jgraph/drawio-desktop/releases/download/v{DRAWIO_VERSION}/drawio-x86_64-{DRAWIO_VERSION}.AppImage',
  'darwin':   f'https://github.com/jgraph/drawio-desktop/releases/download/v{DRAWIO_VERSION}/draw.io-arm64-{DRAWIO_VERSION}.dmg', # TODO need macos extract + execute logic someplace!
  'windows':  f'https://github.com/jgraph/drawio-desktop/releases/download/v{DRAWIO_VERSION}/draw.io-{DRAWIO_VERSION}-windows-no-installer.exe',
}.get(platform.system().lower(), DRAWIO_EXE_UNK_SYS_URL)

def ensure_children_executable(dir_name):
  for child_name in os.listdir(dir_name):
    child_path = os.path.join(dir_name, child_name)
    if os.path.isfile(child_path):
      st = os.stat(child_path)
      os.chmod(child_path, st.st_mode | stat.S_IEXEC)

def idempotent_get_drawio_exe():
  global DRAWIO_EXE_URL
  build_dir = os.path.join(SPD, 'build')
  os.makedirs(build_dir, exist_ok=True)
  os_name = platform.system().lower()
  if 'linux' in os_name:
    linux_exe = os.path.join(build_dir, f'drawio-x86_64-{DRAWIO_VERSION}.AppImage')
    if not os.path.exists(linux_exe):
      print(f'Downloading {DRAWIO_EXE_URL} to {linux_exe}')
      urllib.request.urlretrieve(DRAWIO_EXE_URL, linux_exe)
      ensure_children_executable(build_dir)
    return linux_exe
  elif 'win' in os_name:
    win_exe = os.path.join(build_dir, f'draw.io-{DRAWIO_VERSION}-windows-no-installer.exe')
    if not os.path.exists(win_exe):
      print(f'Downloading {DRAWIO_EXE_URL} to {win_exe}')
      urllib.request.urlretrieve(DRAWIO_EXE_URL, win_exe)
      ensure_children_executable(build_dir)
    return win_exe
  else:
    raise Exception(f'TODO write macos download and extraction from .dmg package! URL = {DRAWIO_EXE_URL}')

def main(args=sys.argv):
  global DRAWIO_EXE_URL

  drawio_exe = idempotent_get_drawio_exe()
  drawio_cmd = [ drawio_exe ]
  if len(args) > 1:
    drawio_cmd.append( args[1] )

  print(f'Command: {" ".join(drawio_cmd)}')
  subprocess.run(drawio_cmd)


if __name__ == '__main__':
  main()

