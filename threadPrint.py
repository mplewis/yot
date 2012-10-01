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

# takes in an OrderedDict of complete threads
# formats and prints the first post from each thread
# the order threads are printed depends on the order of the thread numbers in threadNumList

def printIndex(threadOrderedDict, prefs):
	asciiImagesEnable = prefs["asciiImagesEnable"]
	threadCount = 0
	# OrderedDict iterates by keys, not key-value pairs. It's really silly, imo.
	for threadNum in threadOrderedDict:
		threadCount += 1
		thread = threadOrderedDict[threadNum]
		op = thread.items()[0]
		opData = op[1]
		threadNum = op[0]
		opTextRaw = opData["postText"]
		opTextClean = cleanCommentData(opTextRaw)
		opImageUrl = opData["imageUrl"]
		threadLen = len(thread)
		# if you write a program and say something like "one files remaining",
		# I probably hate you for being lazy.
		postsPluralText = " posts."
		if threadLen == "1":
			postsPluralText = " post."
		# does not check if image url is blank because it
		# assumes op always has a picture. which he does
		if asciiImagesEnable:
			aaFuncs.printUrlToAscii(opImageUrl, prefs["termWidth"])
		print wrap( \
			TermColor.cyan + str(threadCount) + ": " + TermColor.blue + "No. " + str(threadNum) + TermColor.reset + '\n' \
			+ opTextClean + '\n' \
			+ TermColor.blue + str(threadLen) + postsPluralText + TermColor.reset + '\n\n' \
			, prefs["termWidth"])

# takes in a thread in OrderedDict form
# formats and prints all the posts from the given thread

def printThread(threadOrderedDict, prefs):
	asciiImagesEnable = prefs["asciiImagesEnable"]
	print '\n\n'
	for postNum in threadOrderedDict:
		postData = threadOrderedDict[postNum]
		postTextDirty = postData["postText"]
		postTextClean = cleanCommentData(postTextDirty)
		postImageUrl = postData["imageUrl"]
		if asciiImagesEnable and postImageUrl != "":
			aaFuncs.printUrlToAscii(postImageUrl, prefs["termWidth"])
		print wrap( \
			TermColor.cyan + "No. " + str(postNum) + TermColor.reset + '\n' \
			+ postTextClean + '\n\n' \
			, prefs["termWidth"])