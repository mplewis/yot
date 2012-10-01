import urllib2
import json
from collections import OrderedDict

# threadReader takes in:
#     JSON data for one thread (via threadReader().readJson(jsonDataStr))
# threadReader can extract:
#     number of posts, thread (OP post) number, all posts (list: [postNumber, postBodyText])

class ThreadReader(object):
	def __init__(self):
		self.reset()
	def reset(self):
		self.jsonData = []
		self.boardAbbr = ""
		self.op = None
		self.numPosts = 0
		self.allPosts = []
	def setBoardAbbr(self, boardAbbr):
		self.boardAbbr = boardAbbr
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
				postData.append("http://images.4chan.org/" + self.boardAbbr + "/src/" + str(post["tim"]) + post["ext"])
			else:
				postData.append("")
			self.allPosts.append(postData)
	def getNumPosts(self):
		return len(self.jsonData["posts"][0:])
	def getThreadNumber(self):
		return self.op["no"]
	def getAllPosts(self):
		return self.allPosts

# takes in a list of thread numbers from a board's front page and a board abbrev
# returns an ordered data dict of the complete threads from that front page

def parseThreadListToODict(threadNumList, boardAbbr):
	threadDataDict = OrderedDict()
	for threadNum in threadNumList:
		threadUrl = "http://api.4chan.org/" + boardAbbr + "/res/" + str(threadNum) + ".json"
		threadJsonData = urllib2.urlopen(threadUrl).read()
		tRead = ThreadReader()
		tRead.setBoardAbbr(boardAbbr)
		tRead.readJson(threadJsonData)
		threadDataDict[threadNum] = tRead.getAllPosts()
	return threadDataDict