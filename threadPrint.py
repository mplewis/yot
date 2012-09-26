from htmlParse import stripTags
import string

import aaFuncs

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

# FIXME global asciiImagesEnable, asciiImageWidth; is globals the best way to do things?

# takes in a list of thread numbers in order, a dict of complete threads
# formats and prints the first post from each thread
# the order threads are printed depends on the order of the thread numbers in threadNumList

def printIndex(threadNumList, threadDataDict, imgPrefs):
	asciiImagesEnable = imgPrefs["asciiImagesEnable"]
	asciiImageWidth = imgPrefs["asciiImageWidth"]
	threadCount = 0
	for threadNum in threadNumList:
		threadCount += 1
		if threadNum not in threadDataDict:
			raise LookupError("Thread not found: " + str(threadNum))
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
			aaFuncs.printUrlToAscii(opImgUrl, asciiImageWidth)
		print TermColor.cyan + str(threadCount) + ": " + TermColor.blue + "No. " + str(threadNum) + TermColor.reset + '\n' \
			+ opTextClean + '\n' \
			+ TermColor.blue + str(threadLen) + postsPluralText + TermColor.reset + '\n\n'

# takes in a dict of complete threads, a thread number
# formats and prints all the posts from the given thread

def printThread(threadDataDict, threadNum, imgPrefs):
	asciiImagesEnable = imgPrefs["asciiImagesEnable"]
	asciiImageWidth = imgPrefs["asciiImageWidth"]
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
			aaFuncs.printUrlToAscii(postImgUrl, asciiImageWidth)
		print TermColor.cyan + "No. " + str(postNum) + TermColor.reset + '\n' \
			+ postTextClean + '\n\n'