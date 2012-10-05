yot: because console users need 4chan too
=========================================


Written for Python 2 by Matthew Lewis of Kestrel Development.

Allows you to browse the threads on the front page of any 4chan imageboard from a terminal. **Supports *ASCII art* images!**

	usage: yot.py [-h] [-i] [-w WIDTH] board

	positional arguments:
	  board                 the abbreviation of the board to read (ex: r9k, g, tg)

	optional arguments:
	  -h, --help            show this help message and exit
	  -i, --images          enable ASCII image display (default: disabled)
	  -w WIDTH, --width WIDTH
	                        set terminal width in chars for word wrap and ASCII
	                        image display (default: 80 chars)

Python dependencies
-------------------

* aalib
* Python Imaging Library
* argparse
* OrderedDict drop-in (if Python version < 2.7)

but why would you do this thing?
================================

Because I love the terminal, and I love working with APIs, and I love the new 4chan API.

Feel free to send me a pull request if you come up with anything cool.