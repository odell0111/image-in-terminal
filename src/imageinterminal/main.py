import argparse
import logging

from argparse import ArgumentParser
from rich import print
from rich import traceback
from rich.align import Align
from rich.console import Group, Console
from rich.text import Text

from imageinterminal.iit import display_image
from imageinterminal.utils import init_logger
from imageinterminal.custom_rich_help_formatter import CustomRichHelpFormatter

__pname__ = "image-in-terminal"
__version__ = "1.32"
__homepage__ = "https://github.com/odell0111/image-in-terminal"
__author__ = "Odell"
__summary__ = "Simple Python package to display a single or multiple images in the terminal by converting it into text"

logger = logging.getLogger(__name__)


def _parse_args():
  description = [
    Text(__pname__.replace('-', ' ').title(), style='b blink'),
    f"[i]v[bold white]{__version__}[/]",
    f'by {__author__}',
    '2023-2025'
  ]

  # noinspection PyTypeChecker
  parser = ArgumentParser(
    usage="\n  %(prog)s image_uris [options]",
    description=Group(*[Align(line, align='center') for line in description]),
    epilog=f"{__summary__}. For the desired behavior to be achieved, the terminal must support colors, unicode characters and there should be no spacing between lines (0 line-spacing).",
    formatter_class=CustomRichHelpFormatter,
    add_help=False)

  # Options
  parser.add_argument("image_uris", nargs='+', help="File path(s) or HTTP/HTTPS link(s) of the image(s) to be displayed. A directory can also be passed in which case all supported images in the directory will be displayed.")
  parser.add_argument("-w", "--width", metavar='N', type=int, help="Destination width of the image(s).")
  parser.add_argument("-wt", "--whiteness-threshold", metavar='N.', type=float, default=1, help="(float [0 - 1]). Pixels with a whiteness higher than this value will be inverted.")
  parser.add_argument("-dt", "--darkness-threshold", metavar='N.', type=float, default=0, help="(float [0 - 1]). Pixels with a whiteness lower than this value will be inverted.")
  parser.add_argument("-r", "--recursive", action='store_true', help="If a directory is passed as image_uri the image search will be recursively performed within the directory passed and all its subdirectories.")
  parser.add_argument("-pp", "--procedural-printing", action='store_true', help="The image(s) pixels will be printed one by one procedurally instead of printing/displaying the entire image at once. Useful when printing/displaying high resolution images.")
  parser.add_argument("-nc", "--no-center", action='store_true', help="Do not center image(s).")
  parser.add_argument("-nf", "--no-fit", action='store_true', help="Do not automatically fit image(s) width to terminal width when -w/--width is not specified.")
  parser.add_argument("-ll", "--log-level", metavar='N', type=int, default=logging.INFO, help=f"Log level. Default: {logging.INFO}. CRITICAL = 50, FATAL = CRITICAL, ERROR = 40, WARNING = 30, INFO = 20, DEBUG = 10, NOTSET = 0")

  # Miscellaneous Options
  miscellaneous_options = parser.add_argument_group("Miscellaneous")
  miscellaneous_options.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help='Show this help message and exit.')
  miscellaneous_options.add_argument("-v", "--version", action='version', version=f"[argparse.prog]{__pname__}[/] v{__version__}", default=argparse.SUPPRESS, help="Show version number and exit.")

  args = parser.parse_args()
  return args


def main():

  print()

  traceback.install()

  console = Console()

  init_logger(
    console=console,
  )

  args = _parse_args()

  logging.root.setLevel(args.log_level)

  for uri in args.image_uris:
    display_image(
      uri=uri,
      width=args.width if args.width else -1 if args.no_fit else None,
      whiteness_threshold=args.whiteness_threshold,
      darkness_threshold=args.darkness_threshold,
      recursive=args.recursive,
      procedural_printing=args.procedural_printing,
      center=not args.no_center,
      console=console,
      display=True,
    )


if __name__ == '__main__':
  main()
