
# This script takes a shell like bash or cmd.exe and adds
# PATH entries to expose tools in the `tools/` folder as single-word
# commands.

import os
import sys
import subprocess
import platform

HELP_TXT = '''
Commands added:

 - draw.io
    Downoads and runs an OFFLINE version of draw.io from https://github.com/jgraph/drawio-desktop/releases/

'''

DRAWIO_EXE_UNK_SYS_URL = 'https://github.com/jgraph/drawio-desktop/releases/download/v24.7.5/draw.io-24.7.5-windows-no-installer.exe'
DRAWIO_EXE_URL = {
  'linux':    'https://github.com/jgraph/drawio-desktop/releases/download/v24.7.5/drawio-x86_64-24.7.5.AppImage',
  'darwin':   'https://github.com/jgraph/drawio-desktop/releases/download/v24.7.5/draw.io-arm64-24.7.5.dmg', # TODO need macos extract + execute logic someplace!
  'windows':  'https://github.com/jgraph/drawio-desktop/releases/download/v24.7.5/draw.io-24.7.5-windows-no-installer.exe',
}.get(platform.system().lower(), DRAWIO_UNK_SYS_URL)

# Shortcut for SCRIPT_PARENT_DIR - the relative directory holding the python script being executed
SCRIPT_PARENT_DIR = os.path.dirname(__file__)
SPD = SCRIPT_PARENT_DIR

def idempotent_get_drawio_exe():
  global DRAWIO_EXE_URL
  os_name = platform.system().lower()
  if 'linux' in os_name:
    return os.path.join(os.path.dirname(__file__), '')



def main(args=sys.argv):
  global SPD, DRAWIO_EXE_URL

  linux_shell_exe_name = os.environ.get('SHELL', '')

  shell_cmd_to_run = []

  if len(linux_shell_exe_name) > 0:
    shell_cmd_to_run = [ linux_shell_exe_name ]

  tools_dir = os.path.join(SPD, 'tools')
  os.makedirs(tools_dir, exist_ok=True)

  shell_env = dict(os.environ)

  shell_env['PATH'] = os.pathsep.join( os.environ.get('PATH', '').split(os.pathsep) + [ tools_dir ] )

  shell_env['NODE_OPTIONS'] = '--no-warnings '

  if 'WAYLAND_DISPLAY' in os.environ:
    shell_env['ELECTRON_OZONE_PLATFORM_HINT'] = 'wayland'

  print(f'Launching: {" ".join(shell_cmd_to_run)}')
  print()
  print(HELP_TXT.strip())
  print()
  subprocess.run(shell_cmd_to_run, env=shell_env)

if __name__ == '__main__':
  main()

