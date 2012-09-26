#!/usr/bin/python

# shared libraries

import sys
import urllib2
import string

# custom libraries

import userInput
import htmlParse
import threadParse
import threadPrint

# program start!

boardAbbr = userInput.getBoardArgsFirst()
imgPrefs = userInput.getUserImgPrefs()

# orderedThreadNums is a list of the id numbers of the first x threads on the front page of the selected board
orderedThreadNums = htmlParse.fetchBoardThreads(boardAbbr)

# allThreads is a dict that holds data on each thread, because dicts are mostly cooler than lists
allThreads = threadParse.parseThreadListToDict(orderedThreadNums, boardAbbr)
threadPrint.printIndex(orderedThreadNums, allThreads, imgPrefs)

while True:
	commandRaw = raw_input('Enter thread number, "index", or "exit": ')
	command = commandRaw.lower()
	userInput.checkForExit(command)
	if command == "index":
		threadPrint.printIndex(orderedThreadNums, allThreads, imgPrefs)
	else:
		threadNum = -1
		try:
			threadNum = int(command)
			if threadNum in allThreads:
				threadPrint.printThread(allThreads, threadNum, imgPrefs)
			elif threadNum <= len(orderedThreadNums) and threadNum > 0:
				threadPrint.printThread(allThreads, orderedThreadNums[threadNum - 1], imgPrefs)
			else:
				print "Thread not found:", threadNum
		except ValueError:
			print "Not a thread number:", commandRaw