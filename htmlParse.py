from HTMLParser import HTMLParser
import urllib2

# parses the html from a 4chan board index (http(s)://boards.4chan.org/board/[1-10])
# and returns a list of the threads on that page, in order

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

# strips all html and leaves only text data
# nabbed from http://stackoverflow.com/a/925630

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

# takes in a board abbreviation (g, tg, r9k, pol, b, etc.)
# returns a list of the threads on the front page of that board

def fetchBoardThreads(boardAbbr):
	boardUrl = "http://boards.4chan.org/" + boardAbbr + "/1"
	boardParser = ThreadIDParser()
	print "Fetching threads from /" + boardAbbr + "/..." + '\n\n'
	try:
		boardHtmlData = urllib2.urlopen(boardUrl).read()
	except urllib2.HTTPError as currError:
		print "Error accessing board /" + boardAbbr + "/: " + str(currError)
		sys.exit()
	boardParser.feed(boardHtmlData)
	return boardParser.getThreadList()