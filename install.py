import os
import shlex
import subprocess
import sys
from pathlib import Path

import rich
from rich import traceback
import platform
import time
from argparse import ArgumentParser
from rich_argparse import RichHelpFormatter
from shutil import rmtree

_ = traceback.install()
from rich import print
import build

IS_WINDOWS = platform.system() == "Windows"
currentDir = Path(__file__).parent
launcherPath = str(currentDir / 'elevator/launcher.exe')
buildDirPath = currentDir / 'build'

def run(args):
  
  if not IS_WINDOWS:
    parameters = ['sudo']
  else:
    parameters = [str(launcherPath)]
  if isinstance(args, str):
    args = shlex.split(args)
  parameters = parameters + args
  subprocess.run(parameters, check=True)

def parse_args():
  parser = ArgumentParser(description='Simple utility to make a local build while managing required permissions to perform build and install operation',
                          formatter_class=RichHelpFormatter)
  parser.add_argument('-nb', '--no-build', action='store_true', help='Just install, assuming a build is already present')
  parser.add_argument('-d', '--del-build-dir', action='store_true', help='Delete build directory after install')
  parser.add_argument('-t', '--time-to-wait', type=int, default=4, help='Time to wait before exit')
  parser.add_argument('-n', '--no-isolation', action='store_true', help="Disable building the project in an isolated virtual environment. Build dependencies must be installed separately when this option is used")
  return parser.parse_args()


console = rich.console.Console()

args = parse_args()
try:

  if not args.no_build:
    run(f"python -m build {'-n' if args.no_isolation else ''}")
  run('pip install .')
  if args.del_build_dir and buildDirPath.exists():
    rmtree(buildDirPath)
except Exception:
  console.print_exception()

statusText = "Exiting in {}s..."
with console.status('') as status:
  for s in range(args.time_to_wait, 0, -1):
    status.update(statusText.format(s))
    time.sleep(1)
