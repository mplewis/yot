#!/usr/bin/python

# shared libraries

import sys
import urllib2
import string

# custom libraries

import parseArgs
import userInput
import htmlParse
import threadParse
import threadPrint

# quick and dirty functions for internal use; DRY

def displayIndex():
	threadPrint.printIndex(allThreads, userPrefs)

# program start!

userPrefs = dict()
parseArgs.setParsedPrefs(userPrefs)
# userInput.setUserImgPrefs(userPrefs)

boardAbbr = userPrefs["board"]

# orderedThreadNums is a list of the id numbers of  first x threads on the front page of the selected board
orderedThreadNums = htmlParse.fetchBoardThreads(boardAbbr)

# allThreads is an ordered dict that holds data on each thread,
allThreads = threadParse.parseThreadListToODict(orderedThreadNums, boardAbbr)

displayIndex()

while True:
	commandRaw = raw_input('Enter thread number, "index", or "exit": ')
	command = commandRaw.lower()
	userInput.checkForExit(command)
	if command == "index":
		displayIndex()
	else:
		threadNum = -1
		try:
			threadNum = int(command)
			if threadNum in allThreads:
				threadPrint.printThread(allThreads[threadNum], userPrefs)
			elif threadNum <= len(orderedThreadNums) and threadNum > 0:
				# allThreads[allThreads.items()[n - 1][0]] is a hacky way to get
				#     the first element of an nth element of an OrderedDict
				# FIXME this syntax is super dirty, is there a better way to do this?
				threadPrint.printThread(allThreads[allThreads.items()[threadNum - 1][0]], userPrefs)
			else:
				print "Thread not found:", threadNum
		except ValueError:
			print "Not a thread number:", commandRaw