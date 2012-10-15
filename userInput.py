import sys

def checkForExit(command):
	if command == "" or command == "exit" or command == "quit" or command == "q" or command == "x":
		sys.exit()

def menuPrompt():
	commandRaw = raw_input('Enter command, "help", or "exit": ')
	commandLower = commandRaw.lower()
	checkForExit(commandLower)
	return commandLower.split(' ', 1)