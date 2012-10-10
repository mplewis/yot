from HTMLParser import HTMLParser
import urllib2

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)

# strips all html and leaves only text data
# stripTags and MLStripper from http://stackoverflow.com/a/925630
def stripTags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()