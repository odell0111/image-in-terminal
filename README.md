# Image In Terminal

Simple Python package to display an image in the terminal by converting it into text. For the desired behavior to be achieved, the terminal must support colors and there should be no spacing between lines (0 line-spacing).

## Installation
```pip install image-in-terminal``` <br/>

## How to use
You can use the package either from the terminal or from a script.

```
imageinterminal -h

usage:
  imageinterminal image_uris [options]
  iit image_uris [options]

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
  -pp, --procedural-printing
                        The image(s) pixels will be printed one by one procedurally instead of printing/displaying the entire image at
                        once. Useful when printing/displaying high resolution images.
```

**From the terminal:**
```
imageinterminal "myImage.jpg"
iit "https://images/exampleImage.jpg" "myOtherImage.png" -w 128
iit "myImagesOnWhiteBackgrounds" -w 256 -wt 0.97 
```

**From a python script:**
```
from imageinterminal import display_image
display_image("myImage.jpg")
```

## Known Bugs
When the terminal is not zoomed out enough, at least the Windows Terminal, and a large image is printed, it can get bad formatted, as seen in the screenshot. When this happens, simply display the image again. For next time when printing a large image, first zoom out the contents of the terminal, and then display the image 

![](https://raw.githubusercontent.com/odell0111/image-in-terminal/main/Screenshots/bug.png)

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


