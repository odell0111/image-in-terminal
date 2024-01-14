import sys
from pathlib import Path
path = str(Path(__file__).parent) # image-in-terminal/src/imageinterminal
if path not in sys.path:
  sys.path.append(path)

from src.iit import display_image, whiteness, invert_color, main, __version__
