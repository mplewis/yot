import sys

def checkForExit(command):
	if command == "" or command == "exit" or command == "quit" or command == "q" or command == "x":
		sys.exit()

def getBoard():
	return raw_input("Type the abbreviation of the board you wish to browse\n" + \
		"\t(for example: b, g, tg, r9k): ").lower()

# checks first argument for board abbreviation; if not found, prompts user
def getBoardArgsFirst():
	if len(sys.argv) <= 1 or sys.argv[1] == "":
		boardAbbr = getBoard() # already lower case
		checkForExit(boardAbbr)
	else:
		boardAbbr = sys.argv[1]
	return boardAbbr

# takes in a dict of user preferences
# reads user input for image prefs and saves prefs to dictPrefs
def setUserImgPrefs(dictPrefs):
	asciiImagesEnable = False
	imagesYN = raw_input("Enable images? [y/N]: ")
	imagesYNL = imagesYN.lower()
	if imagesYNL == "yes" or imagesYNL == "y":
		asciiImagesEnable = True
	"""
	if asciiImagesEnable == True:
		isIntValue = False
		while isIntValue == False:
			try:
				tempImageWidth = raw_input("Image width (chars) : ")
				intTest = int(tempImageWidth)
				isIntValue = True
			except ValueError:
				print "Invalid image width: " + str(tempImageWidth)
		asciiImageWidth = int(tempImageWidth)
	"""
	# save prefs to dict
	dictPrefs["asciiImagesEnable"] = asciiImagesEnable
	# dictPrefs["asciiImageWidth"] = asciiImageWidth