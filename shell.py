
# This script takes a shell like bash or cmd.exe and adds
# PATH entries to expose tools in the `tools/` folder as single-word
# commands.

import os
import sys
import subprocess
import platform
import stat

HELP_TXT = '''
Commands added:

 - draw.io [/path/to/file.png]
    downloads and runs an OFFLINE version of draw.io from https://github.com/jgraph/drawio-desktop/releases/
    optionally forwards an argument to a .png file

 - draw
    alias for "draw.io"

'''

# Shortcut for SCRIPT_PARENT_DIR - the relative directory holding the python script being executed
SCRIPT_PARENT_DIR = os.environ.get('SCRIPT_PARENT_DIR', os.path.dirname(__file__))
SPD = SCRIPT_PARENT_DIR

def ensure_children_executable(dir_name):
  for child_name in os.listdir(dir_name):
    child_path = os.path.join(dir_name, child_name)
    if os.path.isfile(child_path):
      st = os.stat(child_path)
      os.chmod(child_path, st.st_mode | stat.S_IEXEC)

def main(args=sys.argv):
  global SPD, DRAWIO_EXE_URL

  linux_shell_exe_name = os.environ.get('SHELL', '')

  shell_cmd_to_run = []

  if len(linux_shell_exe_name) > 0:
    shell_cmd_to_run = [ linux_shell_exe_name ]

  tools_dir = os.path.join(SPD, 'tools')
  os.makedirs(tools_dir, exist_ok=True)
  ensure_children_executable(tools_dir)

  shell_env = dict(os.environ)

  shell_env['PATH'] = os.pathsep.join( os.environ.get('PATH', '').split(os.pathsep) + [ tools_dir ] )

  shell_env['SCRIPT_PARENT_DIR'] = SCRIPT_PARENT_DIR

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

