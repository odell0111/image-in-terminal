import argparse
from argparse import ArgumentParser
from importlib import metadata
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image
from rich import print
from rich import traceback
from rich.align import Align
from rich.console import Group, Console
from rich.text import Text

traceback.install()

from src.custom_rich_help_formatter import CustomRichHelpFormatter

__pname__ = "image-in-terminal"
mdata = metadata.metadata(__pname__)
__version__ = mdata['Version']
__homepage__ = mdata['Home-page']
__author__ = mdata['Author']
__summary__ = mdata['Summary']

COMPATIBLE_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'ico']


def whiteness(color):
  '''Returns the whiteness of a color ranging from 0 to 1... how much white a color is'''
  r, g, b = color
  return (r + g + b) / 3 / 255


def invert_color(color):
  r, g, b = color
  r = 255 - r
  g = 255 - g
  b = 255 - b
  return r, g, b


def display_image(uri: str,
                  width: int | None = -1,
                  whiteness_threshold: float = 1,
                  darkness_threshold: float = 0,
                  recursive: bool = False,
                  procedural_printing: bool = False,
                  no_center=False
                  ):
  """
  Displays a single or multiple images in the terminal by converting it into text. For the desired behavior to be achieved, the terminal must support colors, unicode characters and there should be no spacing between lines (0 line-spacing)

  Parameters
  ----------
  uri : str
    File path or HTTP/HTTPS link of the image(s) to be displayed. A directory can also be passed in which case all supported images in the directory will be displayed.

  width : int, optional
    Destination width of the image(s). Leave default to not resize the image(s) or set to None to fit to terminal width

  whiteness_threshold : float
    Pixels with a whiteness higher than this value will be inverted. Ranges from  0 to 1. Default 1

  darkness_threshold : float
    Pixels with a whiteness lower than this value will be inverted. Ranges from  0 to 1. Default 0

  recursive : bool
    If a directory is passed as image_uri the image search will be recursively performed within the directory passed and all its subdirectories

  procedural_printing : bool
    The image pixels will be printed one by one procedurally instead of printing/displaying the entire image at once. Useful when printing/displaying high resolution images

  no_center: bool
    Do not center image(s)

  Returns
  -------
  str
    The image converted to text

  """

  console = Console()
  path = Path(uri)
  filePaths = []
  if path.is_dir():
    for fp in path.glob('**/*.*' if recursive else '*.*'):
      ext = str(fp).split('.')[-1].lower()
      if ext in COMPATIBLE_IMAGE_EXTENSIONS:
        filePaths.append(str(fp))
  else:
    filePaths.append(BytesIO(requests.get(uri).content) if uri.startswith('http') else uri)

  lines = []
  for fp in filePaths:
    img = Image.open(fp)
    img_width, img_height = img.size

    ext = str(fp).split('.')[-1].lower()
    img = img.convert('RGBA' if ext == 'png' else 'RGB')

    # Resizing the image
    if not isinstance(width, int) or width != -1:
      width = max(2, width) if isinstance(width, int) else console.width

      if img_width != width:
        scaleFactor = width / img_width
        new_height = int(img_height * scaleFactor)
        img = img.resize((width, new_height))
        img_width, img_height = img.size

    # Reading 2 rows of pixels each iteration starting form upper left corner
    for y in range(0, img_height - 1, 2):
      twoPixelsHeightLine = ''
      for x in range(img_width):
        # Current pixel will be filled with the visible part (foreground) of the character ▀
        currentPixel = img.getpixel((x, y))[:3]
        # and below pixel will be filled with the transparent part (background) of the character ▀
        belowPixel = img.getpixel((x, y + 1))[:3]

        if (whiteness_threshold < 1 and whiteness(currentPixel) > whiteness_threshold) \
            or (darkness_threshold > 0 and whiteness(currentPixel) < darkness_threshold):
          currentPixel = invert_color(currentPixel)

        if (whiteness_threshold < 1 and whiteness(belowPixel) > whiteness_threshold) \
            or (darkness_threshold > 0 and whiteness(belowPixel) < darkness_threshold):
          belowPixel = invert_color(belowPixel)

        foregroundColor = f"rgb{currentPixel}".replace(' ', '')  # Ex. -> rgb(221,43,12)
        if y == img_height - 1 and img_height % 2 != 0:
          backgroundColor = "black"
        else:
          backgroundColor = f"rgb{belowPixel}".replace(' ', '')

        pixels = f"[{foregroundColor} on {backgroundColor}]▀[/]"
        twoPixelsHeightLine += pixels

      if not no_center and img_width < console.width:
        pad = (console.width - img_width) // 2
        twoPixelsHeightLine = ' ' * pad + twoPixelsHeightLine

      if procedural_printing:
        console.print(twoPixelsHeightLine)

      lines.append(twoPixelsHeightLine)

  lines = '\n'.join(lines)
  if not procedural_printing:
    console.print(lines)
  return lines


def main():
  print()

  description = [Text(__pname__.replace('-', ' ').title(), style='b blink'),
                 f"[i]v[bold white]{__version__}[/]",
                 f'by {__author__}',
                 '2023-2024']

  # noinspection PyTypeChecker
  parser = ArgumentParser(
    usage="\n  %(prog)s image_uris [options]",
    description=Group(*[Align(line, align='center') for line in description]),
    epilog=f"{__summary__}. For the desired behavior to be achieved, the terminal must support colors, unicode characters and there should be no spacing between lines (0 line-spacing).",
    formatter_class=CustomRichHelpFormatter,
    add_help=False)

  # Options
  parser.add_argument("image_uris", nargs='+', help="File path(s) or HTTP/HTTPS link(s) of the image(s) to be displayed. A directory can also be passed in which case all supported images in the directory will be displayed.")
  parser.add_argument("-w", "--width", type=int, help="Destination width of the image(s).")
  parser.add_argument("-wt", "--whiteness-threshold", type=float, default=1, help="(float [0 - 1]). Pixels with a whiteness higher than this value will be inverted.")
  parser.add_argument("-dt", "--darkness-threshold", type=float, default=0, help="(float [0 - 1]). Pixels with a whiteness lower than this value will be inverted.")
  parser.add_argument("-r", "--recursive", action='store_true', help="If a directory is passed as image_uri the image search will be recursively performed within the directory passed and all its subdirectories.")
  parser.add_argument("-pp", "--procedural-printing", action='store_true', help="The image(s) pixels will be printed one by one procedurally instead of printing/displaying the entire image at once. Useful when printing/displaying high resolution images.")
  parser.add_argument("-nc", "--no-center", action='store_true', help="Do not center image(s).")
  parser.add_argument("-nf", "--no-fit", action='store_true', help="Do not automatically fit image(s) width to terminal width when -w/--width is not specified.")

  # Miscellaneous Options
  miscellaneous_options = parser.add_argument_group("Miscellaneous")
  miscellaneous_options.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help='Show this help message and exit.')
  miscellaneous_options.add_argument("-v", "--version", action='version', version=f"[argparse.prog]{__pname__}[/] v{__version__}", default=argparse.SUPPRESS, help="Show version number and exit.")

  args = parser.parse_args()

  for uri in args.image_uris:
    display_image(uri=uri,
                  width=args.width if args.width else -1 if args.no_fit else None,
                  whiteness_threshold=args.whiteness_threshold,
                  darkness_threshold=args.darkness_threshold,
                  recursive=args.recursive,
                  procedural_printing=args.procedural_printing,
                  no_center=args.no_center)


if __name__ == '__main__':
  main()
