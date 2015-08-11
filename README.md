### This is unmaintained :(

I don't have time to maintain this project any more. If you'd like to build on what I have here, feel free!

I'm always available at matt@mplewis.com for questions.

# yot

*because console users need 4chan too*

Written for Python 2.

Allows you to browse the threads on the front page of any 4chan imageboard from a terminal. **Supports *ASCII art* images!**

    usage: yot.py [-h] [-i] [-o] [-w WIDTH] [-t INDENT] [-r WH_RATIO] board

    positional arguments:
      board                 the abbreviation of the board to read (ex: r9k, g, tg)

    optional arguments:
      -h, --help            show this help message and exit
      -i, --images          enable ASCII image display (default: disabled)
      -o, --op-only         only show the first post of each thread on a board's
                            front page, instead of showing the first post and a
                            few replies (default: disabled)
      -w WIDTH, --width WIDTH
                            set terminal width in chars for word wrap and ASCII
                            image display (default: 80 chars)
      -t INDENT, --indent INDENT
                            set indent width in chars for thread replies (default:
                            8 chars)
      -r WH_RATIO, --wh-ratio WH_RATIO
                            set width:height ratio of characters for ASCII image
                            display (default: 0.55)

Make sure you copy `sampleConfig.yml` to `config.yml` so that you have a working default config file. Otherwise, yot will get mad at you when you run it without specifying every argument.

Python dependencies
===================
* [python-aalib](http://jwilk.net/software/python-aalib)
* [Python Imaging Library](http://www.pythonware.com/products/pil/)
* [argparse](http://docs.python.org/library/argparse.html)
* [OrderedDict drop-in](https://github.com/sprintly/ordereddict) (if Python version < 2.7)

but why would you do this thing?
================================

Because I love the terminal, and I love working with APIs, and I love the new 4chan API.

Feel free to send me a pull request if you come up with anything cool.
