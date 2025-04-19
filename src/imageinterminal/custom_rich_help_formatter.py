from rich.console import RenderableType
from rich_argparse import RichHelpFormatter


class CustomRichHelpFormatter(RichHelpFormatter):
  def add_renderable(self, renderable: RenderableType) -> None:
    # padded = r.Padding.indent(renderable, self._current_indent)
    self._current_section.rich_items.append(renderable)
