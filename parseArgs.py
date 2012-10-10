#!/usr/bin/python

import argparse

argParser = argparse.ArgumentParser()
argParser.add_argument("board", help = "the abbreviation of the board to read (ex: r9k, g, tg)")
argParser.add_argument("-i", "--images", help = "enable ASCII image display (default: disabled)", action = "store_true", default = False)
argParser.add_argument("-w", "--width", help = "set terminal width in chars for word wrap and ASCII image display (default: 80 chars)", type = int, default = 80)

# get options from arg parser and put them into a prefs dict
def getParsedPrefs():
	args = argParser.parse_args()
	prefsDict = dict()
	prefsDict["board"] = args.board
	prefsDict["termWidth"] = args.width
	prefsDict["asciiImagesEnable"] = args.images
	return prefsDict