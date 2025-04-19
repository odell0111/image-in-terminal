import logging

import requests

from io import BytesIO
from pathlib import Path
from PIL import Image
from rich.console import Console
from typing import Union, Optional, List

from imageinterminal.constants import COMPATIBLE_IMAGE_FORMATS

logger = logging.getLogger(__name__)


def display_image(
    uri: Union[str, Path],
    width: Optional[int] = None,
    whiteness_threshold: float = 1.0,
    darkness_threshold: float = 0.0,
    recursive: bool = False,
    procedural_printing: bool = False,
    center: bool = True,
    console: Console = Console(),
    display: bool = True,
) -> Optional[str]:
  """
  Convert and display images in terminal as text using Unicode block characters.

  Args:
      uri: Image path/URL or directory containing images
      width: Output width (None for terminal width, omit for original size)
      whiteness_threshold: Invert pixels whiter than this (0-1)
      darkness_threshold: Invert pixels darker than this (0-1)
      recursive: Search subdirectories when processing folders
      procedural_printing: Render progressively for large images
      center: Center images
      console: Rich console instance
      display: Print to console immediately

  Returns:
      String with text representation

  Raises:
      ValueError: For invalid threshold values
  """
  # Validate thresholds
  if not 0 <= darkness_threshold <= whiteness_threshold <= 1:
    logger.error("Thresholds must satisfy 0 <= darkness <= whiteness <= 1")
    return

  # Prepare image sources
  filePaths = _gather_image_sources(
    uri=uri,
    recursive=recursive,
  )
  if filePaths is None:
    return
  if not filePaths:
    logger.error("No valid images found")
    return

  # Process images
  outputLines = []
  for path in filePaths:
    try:
      with Image.open(path) as img:
        outputLines.extend(
          _process_image(
            img=img,
            target_width=width,
            white_thresh=whiteness_threshold,
            dark_thresh=darkness_threshold,
            console=console,
            center=center,
            procedural=procedural_printing,
            display=display,
          )
        )
    except Exception as e:
      logger.error(f"Failed processing {path}: {str(e)}")

  if not outputLines:
    return

  # Join lines
  output = '\n'.join(outputLines)
  # Display
  display and not procedural_printing and console.print(output)
  return output


def _gather_image_sources(
    uri: Union[str, Path],
    recursive: bool,
) -> List[Union[Path, BytesIO]] | None:
  """Collect image sources from various input types."""
  path = Path(uri) if isinstance(uri, str) else uri
  sources = []

  # noinspection HttpUrlsUsage
  if path.is_dir():
    pattern = '**/*' if recursive else '*'
    sources.extend(
      p for p in path.rglob(pattern) if p.suffix.lower() in COMPATIBLE_IMAGE_FORMATS
    )
    logger.debug(f"Found {len(sources)} images in directory")
    return sources

  if str(uri).startswith(('http://', 'https://')):
    try:
      response = requests.get(str(uri), timeout=10)
      response.raise_for_status()
      sources.append(BytesIO(response.content))
      logger.debug(f"Downloaded remote image: {uri}")
      return sources
    except Exception as e:
      logger.error(f"Failed to download {uri}: {e}")
      return

  if path.exists():
    sources.append(path)
    return sources

  logger.error(f"Invalid source: {uri}")


def _process_image(
    img: Image.Image,
    target_width: Optional[int],
    white_thresh: float,
    dark_thresh: float,
    console: Console,
    center: bool,
    procedural: bool,
    display: bool,
) -> List[str]:
  """Process individual image into text lines."""
  # Convert to RGB and resize
  img = img.convert('RGB')
  imgWidth, imgHeight = img.size
  targetWidth = target_width or console.width

  if targetWidth and imgWidth != targetWidth:
    scale = targetWidth / imgWidth
    img = img.resize((targetWidth, int(imgHeight * scale)))
    imgWidth, imgHeight = img.size

  # Precompute color adjustments
  pixels = img.load()
  lines = []

  # Process pixels in pairs of rows
  for y in range(0, imgHeight - 1, 2):
    line = []
    for x in range(imgWidth):
      top = _adjust_pixel(pixels[x, y], white_thresh, dark_thresh)
      bottom = _adjust_pixel(pixels[x, y + 1], white_thresh, dark_thresh)

      fg = f"rgb{top}".replace(' ', '')
      bg = f"rgb{bottom}".replace(' ', '')
      line.append(f"[{fg} on {bg}]▀[/]")

    lineStr = ''.join(line)
    if center and imgWidth < console.width:
      pad = (console.width - imgWidth) // 2
      lineStr = ' ' * pad + lineStr

    # Display pixel
    display and procedural and console.print(lineStr)

    lines.append(lineStr)

  return lines


def _adjust_pixel(pixel: tuple, white_thresh: float, dark_thresh: float) -> tuple:
  """Apply threshold-based color inversion."""
  brightness = sum(pixel) / 765  # 255 * 3
  if brightness > white_thresh or brightness < dark_thresh:
    return 255 - pixel[0], 255 - pixel[1], 255 - pixel[2]
  return pixel
