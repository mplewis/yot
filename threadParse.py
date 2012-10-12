import urllib2
import json

import sys
# OrderedDict introduced in Python 2.7
if sys.version_info[1] >= 7:
	from collections import OrderedDict
else:
	# drop-in substitute for older Python versions
	# http://pypi.python.org/pypi/ordereddict/1.1
	from ordereddict import OrderedDict

# JSON representations of threads and indexes are exposed at the following URLs:
#  http(s)://api.4chan.org/board/res/threadnumber.json
#  http(s)://api.4chan.org/board/pagenumber.json (0 is main index)

def webToStr(url):
	return urllib2.urlopen(url).read()

class Index(object):
	def __init__(self):
		self.reset()
	def reset(self):
		self.jsonData = None
		self.indexData = None
		self.boardAbbr = ""
		self.pageNum = 0
		self.indexJsonUrl = ""
		self.threadList = []

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
		self.jsonData = webToStr(self.indexJsonUrl)
		self.indexData = json.loads(self.jsonData)
		self.threadList = []
		for threadData in self.indexData['threads']:
			threadObj = Thread()
			threadObj.setBoard(self.boardAbbr)
			threadObj.setThreadData(threadData)
			self.threadList.append(threadObj)

	def getAllThreads(self):
		return self.threadList
	def getThread(self, threadNum):
		return self.indexData['threads'][threadNum]

	def getRawJson(self):
		return self.jsonData
	def getJsonObj(self):
		return self.indexData

class Thread(object):
	def __init__(self):
		self.reset()
	def reset(self):
		self.jsonData = None
		self.threadData = None
		self.boardAbbr = ""
		self.threadNum = -1
		self.threadJsonUrl = ""

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

	def updateJsonUrl(self):
		self.threadJsonUrl = 'http://api.4chan.org/' + self.boardAbbr + '/res/' + str(self.threadNum) + '.json'
	def getJsonUrl(self):
		return self.threadJsonUrl
	def refresh(self):
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