import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'src'))

import logging
import pytest

from rich.console import Console
from rich import traceback

from imageinterminal.utils import init_logger

traceback.install()
_console = Console()

init_logger(
  level=logging.DEBUG,
  handler_level=logging.NOTSET,
  force=True,
  console=_console,
  rich_handler=True,
)

logger = logging.getLogger(__name__)
logging.getLogger('faker').setLevel(logging.ERROR)


@pytest.fixture()
def console() -> Console:
  return _console
