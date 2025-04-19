from rich.console import Console

from imageinterminal.iit import display_image


def test_display_image(console: Console):
  imgTxt = display_image(
    uri="ninion.jpg",
    width=None,
    whiteness_threshold=1,
    darkness_threshold=0,
    recursive=False,
    procedural_printing=False,
    center=False,
    console=console,
    display=False,
  )
  console.print(imgTxt)

