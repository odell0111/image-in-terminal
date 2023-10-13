# Image On Terminal

Simple Python package to display an image in the terminal by converting it into text. For the desired behavior to be achieved, the terminal must support colors and there should be no spacing between lines (0 line-spacing).

## Installation
```pip install image-on-terminal``` <br/>

## How to use
You can use the package either from the terminal or from a script.

```
imageonterminal -h

usage:
  imageonterminal image_uris [options]

positional arguments:
  image_uris            File path(s) or HTTP/HTTPS link(s) of the image(s) to be displayed. A directory can also be
                        passed in which case all supported images in the directory will be displayed.

options:
  -h, --help            show this help message and exit
  -w WIDTH, --width WIDTH
                        Destination width of the image(s).
  -wt WHITENESS_THRESHOLD, --whiteness-threshold WHITENESS_THRESHOLD
                        (float [0 - 1]). Pixels with a whiteness higher than this value will be inverted.
  -dt DARKNESS_THRESHOLD, --darkness-threshold DARKNESS_THRESHOLD
                        (float [0 - 1]). Pixels with a whiteness lower than this value will be inverted.
  -r, --recursive       If a directory is passed as image_uri the image search will be recursively performed within
                        the directory passed and all its subdirectories.
```

**From the terminal:**
```
imageonterminal "myImage.jpg"
imageonterminal "https://images/exampleImage.jpg" "myOtherImage.png" -w 128
imageonterminal "myImagesOnWhiteBackgrounds" -w 256 -wt 0.97 
```

**From a python script:**
```
from imageonterminal import display_image
display_image("myImage.jpg")
```

## Screenshots
<div align='center'>
  <p>JPG 256x256</p><br/>
  <img src="https://raw.githubusercontent.com/odell0111/image-on-terminal/main/Screenshots/01.krita_jpg_x256.png"><br/><br/>
  <p>PNG 128x128</p><br/>
  <img src="https://raw.githubusercontent.com/odell0111/image-on-terminal/main/Screenshots/02.am_png_x128.png"><br/><br/>
  <p>PNG 256x256</p><br/>
  <img src="https://raw.githubusercontent.com/odell0111/image-on-terminal/main/Screenshots/03.ar_png_x256.png"><br/><br/>
</div>


