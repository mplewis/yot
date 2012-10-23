import yaml

def loadConfig(file = 'config.yml'):
	with open(file) as cfgFile:
		return yaml.load(cfgFile)