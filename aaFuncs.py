#!/usr/bin/python

import Image
import aalib
import urllib2
from cStringIO import StringIO

# requires Image, aalib
# takes in image streaming object (StringIO or file handle) and image width in terminal chars
# prints the image to the terminal as ascii
def imgToAscii(imgObj, maxAsciiWidth):
	asciiWidthToHeightConstant = 0.55
	imgGrey = imgObj.convert('L') # is now grayscale
	imgSize = imgGrey.size # (width, height)
	imgWidth  = imgSize[0]
	imgHeight = imgSize[1]
	newImageWidth  = 0
	newImageHeight = 0
	# for some reason images render at 1/2 the pixel size of the virtual screen; (width,height)*2 is super hacky but works
	newImageWidth  = maxAsciiWidth * 2
	newImageHeight = (asciiWidthToHeightConstant * maxAsciiWidth / imgWidth) * imgHeight * 2
	# kill the floating points
	newImageWidth  = int(newImageWidth)
	newImageHeight = int(newImageHeight)
	imgResize = imgGrey.resize((newImageWidth, newImageHeight))
	# change AsciiScreen to AnsiScreen or LinuxScreen to get different images
	canvas = aalib.LinuxScreen(width = newImageWidth / 2, height = newImageHeight / 2)
	canvas.put_image((0, 0), imgResize)
	return canvas.render()

# takes in an image url and width in terminal chars
# prints the image to the terminal as ascii
# requires urllib2
def urlToAscii(imgUrl, maxAsciiWidth):
	imgIO = StringIO(urllib2.urlopen(imgUrl).read())
	imgObj = Image.open(imgIO)
	return imgToAscii(imgObj, maxAsciiWidth)