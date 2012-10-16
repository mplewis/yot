#!/usr/bin/python

import argparse

argParser = argparse.ArgumentParser()
argParser.add_argument("board", help = "the abbreviation of the board to read (ex: r9k, g, tg)")
argParser.add_argument("-i", "--images", help = "enable ASCII image display (default: disabled)", action = "store_true", default = False)
argParser.add_argument("-o", "--op-only", help = "only show the first post of each thread on a board's front page, instead of showing the first post and a few replies (default: disabled)", action = "store_true", default = False)
argParser.add_argument("-w", "--width", help = "set terminal width in chars for word wrap and ASCII image display (default: 80 chars)", type = int, default = 80)
argParser.add_argument("-t", "--indent", help = "set indent width in chars for thread replies (default: 8 chars)", type = int, default = 8)
argParser.add_argument("-r", "--wh-ratio", help = "set width:height ratio of characters for ASCII image display (default: 0.55)", type = float, default = 0.55)

# get options from arg parser and put them into a prefs dict
def getParsedPrefs():
	args = argParser.parse_args()
	prefsDict = dict()
	prefsDict['currBoard'] = args.board
	prefsDict['asciiImagesEnable'] = args.images
	prefsDict['ignoreReplies'] = args.op_only
	prefsDict['termWidth'] = args.width
	prefsDict['replyIndent'] = args.indent
	prefsDict['asciiWidthHeightRatio'] = args.wh_ratio
	return prefsDict