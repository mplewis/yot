def boardRefreshFailed(err):
	print "Board refresh failed: " + str(err) + " (is your internet connection OK?)"

def getNewBoardFailed(err):
	print "Get board failed: " + str(err) + " (did you enter the right board abbreviation?)"

def threadLookupFailed(err):
	print "Thread lookup failed: " + str(err)