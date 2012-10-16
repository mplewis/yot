import urllib2
import json
import string

from htmlParse import stripTags

import sys
# OrderedDict introduced in Python 2.7
if sys.version_info[1] >= 7:
	from collections import OrderedDict
else:
	# drop-in substitute for older Python versions
	# http://pypi.python.org/pypi/ordereddict/1.1
	from ordereddict import OrderedDict



# JSON representations of threads and indexes are exposed at the following URLs:
#     http(s)://api.4chan.org/board/res/threadnumber.json
#     http(s)://api.4chan.org/board/pagenumber.json (0 is main index)



def webToStr(url):
	return urllib2.urlopen(url).read()



def purifyCommentData(comment):
	comment = string.replace(comment, "<br>", ' ')
	comment = string.replace(comment, "&gt;", '>')
	comment = string.replace(comment, "&quot;", '"')
	comment = stripTags(comment)
	return comment



class Index(object):
	def __init__(self, boardAbbr = ""):
		self.reset()
		self.setBoard(boardAbbr)
	def reset(self):
		self.iterIndex = -1
		self.jsonData = None
		self.indexData = None
		self.boardAbbr = ""
		self.pageNum = 0
		self.indexJsonUrl = ""
		self.threadList = []

	def __repr__(self):
		return "/" + self.boardAbbr + "/ (" + str(len(self.getAllThreads())) + " posts)"

	def __iter__(self):
		return IndexIter(self)

	def setBoard(self, boardAbbr):
		self.boardAbbr = boardAbbr
		self.updateJsonUrl()
	def setPage(self, pageNum):
		self.pageNum = pageNum
		self.updateJsonUrl()
	def getBoard(self):
		return self.boardAbbr
	def getPage(self):
		return self.pageNum

	def updateJsonUrl(self):
		self.indexJsonUrl = 'http://api.4chan.org/' + self.boardAbbr + '/' + str(self.pageNum) + '.json'
	def getJsonUrl(self):
		return self.indexJsonUrl
	def refresh(self):
		self.updateJsonUrl()
		self.jsonData = webToStr(self.indexJsonUrl)
		self.indexData = json.loads(self.jsonData)
		self.threadList = []
		for threadData in self.indexData['threads']:
			threadObj = Thread()
			threadObj.setBoard(self.boardAbbr)
			threadObj.setThreadData(threadData)
			self.threadList.append(threadObj)

	def getNumThreads(self):
		return len(self.threadList)

	def getAllThreads(self):
		return self.threadList
	def getThread(self, threadNum):
		return self.threadList[threadNum]

	def getRawJson(self):
		return self.jsonData
	def getJsonObj(self):
		return self.indexData

class IndexIter(object):
	def __init__(self, Index):
		self.data = Index.getAllThreads()
		self.pos = -1
	def next(self):
		try:
			self.pos += 1
			return self.data[self.pos]
		except IndexError:
			raise StopIteration



class Thread(object):
	def __init__(self):
		self.reset()
	def reset(self):
		self.iterIndex = -1
		self.jsonData = None
		self.threadData = None
		self.boardAbbr = ""
		self.threadNum = -1
		self.threadJsonUrl = ""

	def __repr__(self):
		if 'com' in self.getOp():
			shortOpText = purifyCommentData(self.getOp()['com'])[0:39]
		else:
			shortOpText = "< no text >"
		return "/" + self.boardAbbr + "/" + str(self.threadNum) + " (" + str(self.getNumReplies()) + "r, " + str(self.getNumImageReplies()) + "i): \"" + shortOpText + '"'

	def __iter__(self):
		return ThreadIter(self)

	def setThreadData(self, threadData):
		self.threadData = threadData
		self.getThreadNumFromSelf()
	def feedThreadJson(self, jsonData):
		self.threadData = json.loads(jsonData)
		self.getThreadNumFromSelf()
	def getThreadNumFromSelf(self):
		self.threadNum = self.threadData['posts'][0]['no']

	def setBoard(self, boardAbbr):
		self.boardAbbr = boardAbbr
		self.updateJsonUrl()
	def setNum(self, threadNum):
		self.threadNum = threadNum
		self.updateJsonUrl()
	def getBoard(self):
		return self.boardAbbr
	def getNum(self):
		return self.threadNum

	def getNumReplies(self):
		return len(self.getAllPosts()) + self.getNumPostsOmitted()
	def getNumImageReplies(self):
		images = 0
		for post in self.getAllPosts():
			if 'tim' in post:
				images += 1
		return images + self.getNumImagesOmitted()
	def getNumPostsOmitted(self):
		if 'omitted_posts' in self.getOp():
			return self.getOp()['omitted_posts']
		else:
			return 0
	def getNumImagesOmitted(self):
		if 'omitted_images' in self.getOp():
			return self.getOp()['omitted_images']
		else:
			return 0

	def updateJsonUrl(self):
		self.threadJsonUrl = 'http://api.4chan.org/' + self.boardAbbr + '/res/' + str(self.threadNum) + '.json'
	def getJsonUrl(self):
		return self.threadJsonUrl
	def refresh(self):
		self.updateJsonUrl()
		self.jsonData = webToStr(self.threadJsonUrl)
		self.threadData = json.loads(self.jsonData)
		
	def getAllPosts(self):
		return self.threadData['posts']
	def getPost(self, postNum):
		return self.threadData['posts'][postNum]
	def getOp(self):
		return self.threadData['posts'][0]
	def getReplies(self):
		return self.threadData['posts'][1:]

	def getRawJson(self):
		return json.dumps(self.threadData)
	def getJsonObj(self):
		return self.threadData

class ThreadIter(object):
	def __init__(self, Thread):
		self.data = Thread.getAllPosts()
		self.pos = -1
	def next(self):
		try:
			self.pos += 1
			return self.data[self.pos]
		except IndexError:
			raise StopIteration



def getFullThreadViaIndex(index, threadNum):
	try:
		threadNum = int(threadNum)
	except ValueError:
		raise ValueError('Not a valid thread number: "' + threadNum + '"')

	if threadNum <= index.getNumThreads() and threadNum > 0:
		thread = index.getThread(threadNum - 1)
		if thread.getNumPostsOmitted() != 0:
			thread.refresh()
		return thread
	else:
		raise LookupError('Thread index out of range: ' + str(threadNum) + \
			': must be from 1 to ' + str(index.getNumThreads()))