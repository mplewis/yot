from htmlParse import stripTags
import string

import aaFuncs
from wrapLine import wrap

# defines terminal colors for Linux terminals
# used to format 4chan text posts all fancy-like

class TermColor:
	red   = '\033[31m' 
	green = '\033[32m'
	blue  = '\033[34m'
	cyan  = '\033[36m'
	reset = '\033[0m'

# takes in a raw text+html comment from a 4chan post
# returns a comment without <span>, <br>, &gt;, etc.; removes them or replaces with color formatting

def cleanCommentData(comment):
	# FIXME bluetext for >>8675309 / >>>/g/7654321 type quotes stays blue until newline;
	#     this affects just posts with body text after >> and >>>
	comment = string.replace(comment, "&gt;&gt;&gt;", TermColor.blue + '>>>')
	comment = string.replace(comment, "&gt;&gt;", TermColor.blue + '>>')
	comment = string.replace(comment, "<br>", '\n' + TermColor.reset)
	comment = string.replace(comment, "&gt;", '>')
	comment = string.replace(comment, "&quot;", '"')
	comment = string.replace(comment, '<span class="quote">', TermColor.green)
	comment = string.replace(comment, '</span>', TermColor.reset)
	comment = stripTags(comment)
	return comment

# takes in a list of thread numbers in order, a dict of complete threads
# formats and prints the first post from each thread
# the order threads are printed depends on the order of the thread numbers in threadNumList

def printIndex(threadOrderedDict, prefs):
	asciiImagesEnable = prefs["asciiImagesEnable"]
	asciiImageWidth = prefs["asciiImageWidth"]
	threadCount = 0
	for threadNum in threadOrderedDict:
		threadCount += 1
		thread = threadOrderedDict[threadNum]
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
			aaFuncs.printUrlToAscii(opImgUrl, asciiImageWidth)
		print wrap( \
			TermColor.cyan + str(threadCount) + ": " + TermColor.blue + "No. " + str(threadNum) + TermColor.reset + '\n' \
			+ opTextClean + '\n' \
			+ TermColor.blue + str(threadLen) + postsPluralText + TermColor.reset + '\n\n' \
			, 80)

# takes in a thread in list form
# formats and prints all the posts from the given thread

def printThread(thread, prefs):
	asciiImagesEnable = prefs["asciiImagesEnable"]
	asciiImageWidth = prefs["asciiImageWidth"]
	print '\n\n'
	for post in thread:
		postNum = post[0]
		postTextDirty = post[1]
		postTextClean = cleanCommentData(postTextDirty)
		postImgUrl = post[2]
		if asciiImagesEnable and postImgUrl != "":
			aaFuncs.printUrlToAscii(postImgUrl, asciiImageWidth)
		print wrap( \
			TermColor.cyan + "No. " + str(postNum) + TermColor.reset + '\n' \
			+ postTextClean + '\n\n' \
			, 80)