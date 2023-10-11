from setuptools import setup
from imageonterminal.__version__ import __version__

setup(
  name='ImageOnTerminal',
  version=__version__,
  packages=['imageonterminal', 'imageonterminal.src'],
  url='https://github.com/odell0111/image-on-terminal',
  license='MIT',
  author='Odell',
  keywords='terminal image imageonterminal imageinterminal imageonconsole imageinconsole imagetotext',
  author_email='odellgm11012001@gmail.com',
  install_requires=['PIP',
                    'rich',
                    'requests',
                    'argparse',
                    'pathlib'],
  description='Simple Python package to display an image in the terminal by converting it into text.',
  long_description='Simple Python package to display an image in the terminal by converting it into text. For the desired behavior to be achieved, the terminal must support colors and there should be no spacing between lines (0 line-spacing).'
)
