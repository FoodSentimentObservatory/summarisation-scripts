from configparser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config.txt')

def resultsPath():
	path = parser.get('folder-paths', 'results')
	return path

def rawTweetsPath():
	path = parser.get('folder-paths', 'rawTwees')	
	return path

def getDocumentPi():
	documentPiFile = parser.get('file-paths', 'documentPi')
	return documentPiFile

def getTopicWordsFile():
	topicWordFile = parser.get('file-paths', 'topicWords')
	return 	topicWordFile

def getTopicSentencesFile():
	topicSentencesFile = parser.get('file-paths', 'topicSentences')
	return 	topicSentencesFile

def getDocumentThethaFile():
	documentThethaFile = parser.get('file-paths', 'documentThetha')
	return 	documentThethaFile