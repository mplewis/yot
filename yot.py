#!/usr/bin/python

# FIXME make this program not a monolithic piece of design failure

import sys
from HTMLParser import HTMLParser
import urllib2
import json
import string
import Image
import aalib
from cStringIO import StringIO

# class and function definition

class TermColor:
	red   = '\033[31m' 
	green = '\033[32m'
	blue  = '\033[34m'
	cyan  = '\033[36m'
	reset = '\033[0m'

class ThreadIDParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.reset()
	def reset(self):
		HTMLParser.reset(self)
		self.threadList = []
	def handle_starttag(self, tag, attrs):
		if tag == "div":
			for attr in attrs:
				if attr[0] == "class" and attr[1] == "thread":
					for attr in attrs:
						if attr[0] == "id":
							rawThreadID = attr[1]
							cleanThreadID = int(attr[1][1:])
							self.threadList.append(cleanThreadID)
	def getThreadList(self):
		return self.threadList

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)

def stripTags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()

def cleanCommentData(comment):
	# FIXME bluetext for >>8675309 type quotes stays blue until newline;
	#     this affects just a few posts
	comment = string.replace(comment, "&gt;&gt;&gt;", TermColor.blue + '>>')
	comment = string.replace(comment, "&gt;&gt;", TermColor.blue + '>>')
	comment = string.replace(comment, "<br>", '\n' + TermColor.reset)
	comment = string.replace(comment, "&gt;", '>')
	comment = string.replace(comment, "&quot;", '"')
	comment = string.replace(comment, '<span class="quote">', TermColor.green)
	comment = string.replace(comment, '</span>', TermColor.reset)
	comment = stripTags(comment)
	return comment

# threadReader takes in:
#     JSON data for one thread (via threadReader().readJson(jsonDataStr))
# threadReader can extract:
#     number of posts, thread (OP post) number, all posts (list: [postNumber, postBodyText])

class ThreadReader(object):
	def __init__(self):
		self.reset()
	def reset(self):
		self.jsonData = []
		self.op = None
		self.numPosts = 0
		self.allPosts = []
	def readJson(self, rawJsonData):
		self.jsonData = json.loads(rawJsonData)
		self.op = self.jsonData["posts"][0]
		for post in self.jsonData["posts"]:
			# postData holds info about each post
			# data comes in the form of [postNum, postText, filename]
			postData = []
			postData.append(post["no"])
			# if post is textless, dict "post" will not have a key "com"
			if "com" in post:
				postData.append(post["com"])
			else:
				postData.append("< no text >")
			# if image is present, keys "tim" and "ext" show up in dict
			if "tim" in post:
				postData.append("http://images.4chan.org/" + boardAbbr + "/src/" + str(post["tim"]) + post["ext"])
			else:
				postData.append("")
			self.allPosts.append(postData)
	def getNumPosts(self):
		return len(self.jsonData["posts"][0:])
	def getThreadNumber(self):
		return self.op["no"]
	def getAllPosts(self):
		return self.allPosts

def parseThreadListToDict(threadNumList, threadDataDict):
	for threadNum in threadNumList:
		threadUrl = "http://api.4chan.org/" + boardAbbr + "/res/" + str(threadNum) + ".json"
		threadJsonData = urllib2.urlopen(threadUrl).read()
		tRead = ThreadReader()
		tRead.readJson(threadJsonData)
		threadDataDict[threadNum] = tRead.getAllPosts()

def printIndex(threadNumList, threadDataDict):
	threadCount = 0
	for threadNum in threadNumList:
		threadCount += 1
		thread = threadDataDict[threadNum]
		op = thread[0]
		threadNum = op[0]
		opTextRaw = op[1]
		opTextClean = cleanCommentData(opTextRaw)
		opImgUrl = op[2]
		threadLen = len(thread)
		postsPluralText = " posts."
		if threadLen == "1":
			postsPluralText = " post."
		if asciiImagesEnable: # assumes op always has a picture. which he does
			printUrlToAscii(opImgUrl, asciiImageWidth)
		print TermColor.cyan + str(threadCount) + ": " + TermColor.blue + "No. " + str(threadNum) + TermColor.reset + '\n' \
			+ opTextClean + '\n' \
			+ TermColor.blue + str(threadLen) + postsPluralText + TermColor.reset + '\n\n'
	# print "Threads:", orderedThreadNums


def printThread(threadDataDict, threadNum):
	if threadNum not in threadDataDict:
		raise LookupError("Thread not found: " + str(threadNum))
	print '\n\n'
	threadPosts = threadDataDict[threadNum] # list of [postNum, postText] lists
	for post in threadPosts:
		postNum = post[0]
		postTextDirty = post[1]
		postTextClean = cleanCommentData(postTextDirty)
		postImgUrl = post[2]
		if asciiImagesEnable and postImgUrl != "":
			printUrlToAscii(postImgUrl, asciiImageWidth)
		print TermColor.cyan + "No. " + str(postNum) + TermColor.reset + '\n' \
			+ postTextClean + '\n\n'

# requires Image, aalib
# takes in image streaming object (StringIO or file handle)
def printImgToAscii(imgObj, maxAsciiWidth):
	asciiWidthToHeightConstant = 0.55
	imgGrey = imgObj.convert('L') # is now grayscale
	imgSize = imgGrey.size # (width, height)
	imgWidth  = imgSize[0]
	imgHeight = imgSize[1]
	newImageWidth  = 0
	newImageHeight = 0
	# for some reason images render at 1/2 the pixel size of the virtual screen; (width,height)*2 is super hacky but works
	newImageWidth  = maxAsciiWidth * 2
	newImageHeight = (asciiWidthToHeightConstant * maxAsciiWidth / imgWidth) * imgHeight * 2
	# kill the floating points
	newImageWidth  = int(newImageWidth)
	newImageHeight = int(newImageHeight)
	imgResize = imgGrey.resize((newImageWidth, newImageHeight))
	# change AsciiScreen to AnsiScreen or LinuxScreen to get different images
	canvas = aalib.LinuxScreen(width = newImageWidth / 2, height = newImageHeight / 2)
	canvas.put_image((0, 0), imgResize)
	print canvas.render()

def printUrlToAscii(imgUrl, maxAsciiWidth):
	imgIO = StringIO(urllib2.urlopen(imgUrl).read())
	imgObj = Image.open(imgIO)
	printImgToAscii(imgObj, maxAsciiWidth)

def fetchBoardThreads(boardAbbr):
	boardUrl = "http://boards.4chan.org/" + boardAbbr + "/1"
	boardParser = ThreadIDParser()
	print "Fetching threads from /" + boardAbbr + "/..."
	try:
		boardHtmlData = urllib2.urlopen(boardUrl).read()
	except urllib2.HTTPError as currError:
		print "Error accessing board /" + boardAbbr + "/: " + str(currError)
		sys.exit()
	boardParser.feed(boardHtmlData)
	return boardParser.getThreadList()

def getBoard():
	return raw_input("Type the abbreviation of the board you wish to browse\n" + \
		"\t(for example: b, g, tg, r9k): ").lower()

def getBoardArgsFirst():
	if len(sys.argv) <= 1 or sys.argv[1] == "":
		boardAbbr = getBoard() # already lower case
		checkForExit(boardAbbr)
	else:
		boardAbbr = sys.argv[1]
	return boardAbbr

def getUserImgPrefs():
	global asciiImagesEnable
	global asciiImageWidth
	imagesYN = raw_input("Enable images? [y/N]: ")
	imagesYNL = imagesYN.lower()
	if imagesYNL == "yes" or imagesYNL == "y":
		asciiImagesEnable = True
	if asciiImagesEnable == True:
		isIntValue = False
		while isIntValue == False:
			try:
				tempImageWidth = raw_input("Image width (chars) : ")
				intTest = int(tempImageWidth)
				isIntValue = True
			except ValueError:
				print "Invalid image width: " + str(tempImageWidth)
		asciiImageWidth = int(tempImageWidth)

def checkForExit(command):
	if command == "" or command == "exit" or command == "quit" or command == "q" or command == "x":
		sys.exit()

# program start!

asciiImagesEnable = False
asciiImageWidth   = -1

boardAbbr = getBoardArgsFirst()
getUserImgPrefs()

# orderedThreadNums is a list of the id numbers of the first x threads on the front page of the selected board
orderedThreadNums = fetchBoardThreads(boardAbbr)

# allThreads is a dict that holds data on each thread, because dicts are mostly cooler than lists
allThreads = dict()

parseThreadListToDict(orderedThreadNums, allThreads)
printIndex(orderedThreadNums, allThreads)

while True:
	commandRaw = raw_input('Enter thread number, "index", or "exit": ')
	command = commandRaw.lower()
	checkForExit(command)
	if command == "index":
		printIndex(orderedThreadNums, allThreads)
	else:
		threadNum = 0
		try:
			threadNum = int(command)
			if threadNum in allThreads:
				printThread(allThreads, threadNum)
			elif threadNum <= len(orderedThreadNums) and threadNum > 0:
				printThread(allThreads, orderedThreadNums[threadNum - 1])
			else:
				print "Thread not found:", threadNum
		except ValueError:
			print "Not a thread number:", commandRaw