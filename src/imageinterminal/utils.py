import logging

from rich.console import Console
from rich.logging import RichHandler


def init_logger(
    console: Console | None = None,
    level: int | str = logging.INFO,
    handler_level: int | str = logging.NOTSET,
    force: bool = False,
    rich_handler: bool = True,
):

  richHandler = RichHandler(
    level=handler_level,
    markup=True,
    show_path=False,
    log_time_format='[%X]',
    console=console,
    rich_tracebacks=True,
  ) if rich_handler else None

  logging.basicConfig(
    level=level,
    format="%(message)s",
    datefmt="[%X]",
    force=force,
    handlers=[richHandler] if rich_handler else None,
  )
