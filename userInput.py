import sys

def checkForExit(command):
	if command == "" or command == "exit" or command == "quit" or command == "q" or command == "x":
		sys.exit()