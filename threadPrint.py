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
	# FIXME make this take care of [code][/code] and [spoiler][/spoiler] tags
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

def printIndex(index):
	replyIndent = 8
	threadCount = 0
	for thread in index.getAllThreads():
		threadCount += 1
		op = thread.getOp()
		opNum = op['no']
		opTime = op['now']
		textPostsOmitted = ""
		if 'omitted_posts' in op:
			textPostsOmitted += TermColor.blue + str(op['omitted_posts'])
			if op['omitted_posts'] == 1:
				textPostsOmitted += " reply "
			else:
				textPostsOmitted += " replies "
			if 'omitted_images' in op:
				if op['omitted_images'] > 0:
					textPostsOmitted += "and " + str(op['omitted_images'])
					if op['omitted_images'] == 1:
						textPostsOmitted += " image reply "
					else:
						textPostsOmitted += " image replies "
			textPostsOmitted += "omitted." + TermColor.reset + "\n"
		opTextRaw = op['com']
		opTextClean = cleanCommentData(opTextRaw)
		replies = thread.getReplies()
		print wrap( \
			TermColor.cyan + str(threadCount) + ": No. " + str(opNum) + TermColor.reset + '\n' \
			+ opTextClean + '\n' \
			+ textPostsOmitted + '\n' \
			, 80)

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