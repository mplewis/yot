#!/usr/bin/python

import string
from urllib2 import HTTPError

import userInput
import parseArgs
import threadParse
import threadPrint
import msgPrint
import errorPrint

def safeNewBoard(index, board):
	index.setBoard(board)
	try:
		index.refresh()
	except HTTPError, err:
		errorPrint.getNewBoardFailed(err)
	else:
		threadPrint.printIndex(index, prefs)

def safeRefresh(index):
	try:
		index.refresh()
	except HTTPError, err:
		errorPrint.boardRefreshFailed(err)
	else:
		threadPrint.printIndex(index, prefs)

prefs = parseArgs.getParsedPrefs()
currBoard = prefs['currBoard']

index = threadParse.Index()
safeNewBoard(index, currBoard)

threadPrint.printIndex(index, prefs)

while True:
	action = userInput.menuPrompt()
	if action[0] == 'help' or action[0] == 'h' or action[0] == '?':
		msgPrint.help()
	elif action[0] == 'index' or action[0] == 'i':
		threadPrint.printIndex(index, prefs)
	elif action[0] == 'refresh' or action[0] == 'r':
		safeRefresh(index)
	elif action[0] == 'board' or action[0] == 'b':
		safeNewBoard(index, action[1])
	elif action[0] == 'thread' or action[0] == 't':
		try:
			threadPrint.printThread(threadParse.getFullThreadViaIndex(index, action[1]), prefs)
		except ValueError, err:
			errorPrint.invalidThreadNum(err)
		except LookupError, err:
			errorPrint.invalidThreadNum(err)
	else:
		try:
			threadPrint.printThread(threadParse.getFullThreadViaIndex(index, action[0]), prefs)
		except Exception:
			print 'Command not recognized: "' + string.join(action) + '"'