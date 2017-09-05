from configparser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config.txt')

def resultsPath():
	path = parser.get('folder-paths', 'results')
	return path

def rawTweetsPath():
	path = parser.get('folder-paths', 'rawTwees')	
	return path

	