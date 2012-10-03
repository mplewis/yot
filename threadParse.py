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

# threadReader takes in:
#     JSON data for one thread (via threadReader().readJson(jsonDataStr))
# threadReader can extract:
#     number of posts, thread (OP post) number,
#     all posts (OrderedDict: (postNum, postDataDict))

class ThreadReader(object):
	def __init__(self):
		self.reset()
	def reset(self):
		self.jsonData = None
		self.boardAbbr = ""
		self.op = None
		self.numPosts = 0
		self.allPosts = OrderedDict()
	def setBoardAbbr(self, boardAbbr):
		self.boardAbbr = boardAbbr
	def readJson(self, rawJsonData):
		self.jsonData = json.loads(rawJsonData)
		self.op = self.jsonData["posts"][0]
		for post in self.jsonData["posts"]:
			# postData is a dict which holds info about each post
			#     postNum: post number
			#     postText: post body
			#     imageUrl: url of posted image
			postData = dict()
			# if post is textless, dict "post" will not have a key "com"
			if "com" in post:
				postData["postText"] = post["com"]
			else:
				postData["postText"] = "< no text >"
			# if image is present, keys "tim" and "ext" show up in dict
			if "tim" in post:
				postData["imageUrl"] = "http://images.4chan.org/" + self.boardAbbr + "/src/" + str(post["tim"]) + post["ext"]
			else:
				postData["imageUrl"] = ""
			# store the post data dict as a key, value pair in the allPosts OrderedDict
			#     key = postNum
			#     value = postDataDict
			self.allPosts[post["no"]] = postData
	def getNumPosts(self):
		return len(self.jsonData["posts"])
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