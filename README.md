<div align="center">
  <a href='https://pypi.org/project/image-in-terminal'>
    <img src="https://img.shields.io/pypi/v/image-in-terminal?label=PyPI%20Package">
  </a>
  <img src="https://static.pepy.tech/badge/image-in-terminal/month"/>
  <h2>Image In Terminal</h2>
</div>

Simple Python package to display an image in the terminal by converting it into text. For the desired behavior to be achieved, the terminal must support colors, unicode characters and there should be no spacing between lines (0 line-spacing).

## Installation
```pip install image-in-terminal``` <br/>

## How to use
You can use the package either from the terminal or from a script.

```console
imageinterminal -h

Usage:
  imageinterminal image_uris [options]

                                                  Image In Terminal
                                                        v1.2.6
                                                       by Odell
                                                      2023-2024
Positional Arguments:
  image_uris            File path(s) or HTTP/HTTPS link(s) of the image(s) to be displayed. A directory can also be
                        passed in which case all supported images in the directory will be displayed.

Options:
  -w, --width WIDTH     Destination width of the image(s).
  -wt, --whiteness-threshold WHITENESS_THRESHOLD
                        (float [0 - 1]). Pixels with a whiteness higher than this value will be inverted.
  -dt, --darkness-threshold DARKNESS_THRESHOLD
                        (float [0 - 1]). Pixels with a whiteness lower than this value will be inverted.
  -r, --recursive       If a directory is passed as image_uri the image search will be recursively performed within
                        the directory passed and all its subdirectories.
  -pp, --procedural-printing
                        The image(s) pixels will be printed one by one procedurally instead of printing/displaying the
                        entire image at once. Useful when printing/displaying high resolution images.
  -nc, --no-center      Do not center image(s).
  -nf, --no-fit         Do not automatically fit image(s) width to terminal width when -w/--width is not specified.

Miscellaneous:
  -h, --help            Show this help message and exit.
  -v, --version         Show version number and exit.

Simple Python package to display a single or multiple images in the terminal by converting it into text. For the
desired behavior to be achieved, the terminal must support colors, unicode characters and there should be no spacing
between lines (0 line-spacing).
```

**From the terminal:**
```bash
imageinterminal "myImage.jpg"
iit "https://images/exampleImage.jpg" "myOtherImage.png" -w 128
iit "myImagesOnWhiteBackgrounds" --width 256 -wt 0.97 
iit myImage2.png --no-fit --no-center
```

**From a python script:**
```python
from imageinterminal import display_image
display_image("myImage.jpg")
```

## Donate

<a href="https://oxapay.com/donate/42319117" target="_blank"> <img src="https://app.oxapay.com/media/btn/light-btn.png" style="width: 200px"> </a>

### TON
```
UQAtE6g_gxHgDoD_rzR_lHqBN9zbR9367U1Mxu21F7c3CPI5
```
### Bitcoin
```
bc1qvnu237er6rxt8cazze6lx3dme66n60gjwgh2mx
```
#### Speed Lightning Address username
```
bytechanger@speed.app
```

<div align='center'>
  <h2>Screenshots</h2>
  <p>JPG 1440x1800</p><br/>
  <img src="https://raw.githubusercontent.com/odell0111/image-in-terminal/main/Screenshots/animal_png_x1440.png"><br/><br/>
  <p>JPG 256x256</p><br/>
  <img src="https://raw.githubusercontent.com/odell0111/image-in-terminal/main/Screenshots/krita_jpg_x256.png"><br/><br/>
  <p>PNG 256x256</p><br/>
  <img src="https://raw.githubusercontent.com/odell0111/image-in-terminal/main/Screenshots/ar_png_x256.png"><br/><br/>
  <p>Procedural Printing</p><br/>
  <img src="https://raw.githubusercontent.com/odell0111/image-in-terminal/main/Screenshots/procedural_printing.gif"><br/><br/>
</div>


