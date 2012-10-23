#!/usr/bin/python
import argparse
from loadConfig import loadConfig

argParser = argparse.ArgumentParser()
argParser.add_argument("board", help = "the abbreviation of the board to read (ex: r9k, g, tg)")
argParser.add_argument("-i", "--images", help = "enable ASCII image display", action = "store_true", default = None)
argParser.add_argument("-o", "--op-only", help = "only show the first post of each thread on a board's front page, instead of showing the first post and a few replies", action = "store_true", default = None)
argParser.add_argument("-w", "--width", help = "set terminal width in chars for word wrap and ASCII image display", type = int)
argParser.add_argument("-t", "--indent", help = "set indent width in chars for thread replies", type = int)
argParser.add_argument("-r", "--wh-ratio", help = "set width:height ratio of characters for ASCII image display", type = float)

# get options from arg parser and put them into a prefs dict
def getParsedPrefs():
	cfg = loadConfig()
	args = argParser.parse_args()
	prefsDict = dict()
	prefsDict['currBoard'] = args.board
	if args.images == None:
		prefsDict['asciiImagesEnable'] = cfg['images']['enableAsciiImages']
	else:
		prefsDict['asciiImagesEnable'] = args.images
	if args.op_only == None:
		prefsDict['ignoreReplies'] = cfg['display']['onlyShowOP']
	else:
		prefsDict['ignoreReplies'] = args.op_only
	if args.width == None:
		prefsDict['termWidth'] = cfg['display']['terminalWidth']
	else:
		prefsDict['termWidth'] = args.width
	if args.indent == None:
		prefsDict['replyIndent'] = cfg['display']['replyIndent']
	else:
		prefsDict['replyIndent'] = args.indent
	if args.wh_ratio == None:
		prefsDict['asciiWidthHeightRatio'] = cfg['images']['asciiWidthHeightRatio']
	else:
		prefsDict['asciiWidthHeightRatio'] = args.wh_ratio
	return prefsDict