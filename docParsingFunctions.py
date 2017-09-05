import sys
import os
from operator import itemgetter
from itertools import groupby
import re
from configparser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config.txt')
#functions used by doc topics and topic importance
def mainTopics():
	topTopics=[]
	documentThethaFile = parser.get('file-paths', 'documentThetha')
	doc = open (documentThethaFile, "r")
	lines = [line.split() for line in doc.readlines()]
	i=0
	#each line gets an assignment
	docIndex = ""
	for line in lines:
		pos = []
		neg =[]
		neu = []
		topicsAndLabels = []
		if "Document" in line:
			docIndex = line
			i = 1
		#using a counter i to identify each line that belongs to a document	
		elif i == 1:
			neutral = []
			mneu = 0
			value = "neutral"
			topicLabels(value,line, topicsAndLabels)
			listAppend (docIndex, topTopics, topicsAndLabels, neu, neutral, mneu, value)
			i = 2
		elif i ==2:
			positive = []
			mpos =0
			value = "positive"
			topicLabels(value,line, topicsAndLabels)
			listAppend (docIndex, topTopics, topicsAndLabels, pos, positive, mpos, value)
			i = 3
		else:
			negative = []
			mneg = 0
			value = "negative"
			topicLabels(value,line, topicsAndLabels)
			listAppend(docIndex, topTopics, topicsAndLabels,neg,negative, mneg, value)
			i=0		
	return topTopics
#function to generate topic labels for easier mapping to documents
def topicLabels(value, line, topicsAndLabels):
	i = 0 #count for label
	if value == "neutral":
		i = 0
	elif value == "positive":
		i = 1	
	else:
		i = 2	
	n=0	 #count for topic
	#generating a name using the count for sentiment, i, and the count for topic, n
	for topic in line:
			label = "Label"+str(i)
			topicN = "Topic"+str(n)
			topicLabel = label +"_"+ topicN
			topicTuple = (topicLabel, topic)
			topicsAndLabels.append(topicTuple)	
			n += 1	
#function to collect the sentiment scores for each document
def mainSentiment():
	topSents = []
	documentPiFile = parser.get('file-paths', 'documentPi')
	doc = open (documentPiFile, "r")
	lines = [line.split() for line in doc.readlines()]
	topSentiment = 0

	for line in lines:
		sentValueList = []
		i = 0
		docIndex = re.sub(r'[<d_>\s]', '', str(line[0]))
		docName = line[1]
		for item in line:
		#each sentiment value is saved as a separate sublist with the corresponsing doc name and sentiment label 	
			if "d_" not in item:
				if i == 2:
					value = "neutral"
				elif i == 3:
					value = "positive"
				else:
					value = "negative"		
				sentDoc = (docIndex, docName,value, item)
				sentValueList.append(sentDoc)
			i += 1	
		#a list of sentiment sublists is created and sorted by the sentiment value for each document	
		sortedSents = sorted(sentValueList, key=itemgetter(3), reverse = True)	
		#that sorted list is added to a final list of all sentiment values accros all docs
		topSents.append(sortedSents)
	return topSents	
#function to select the topic with the highest probability score for each sentiment and save the scores for each document in a list
def listAppend (docIndex,topTopics ,line, lineList, sentiment, mtop, value):
	lineList.append(line)
	sentiment = sorted(line, key=itemgetter(1), reverse = True)			
	mtop = sentiment[0]
	sentTop = [docIndex,value,sentiment]
	topTopics.append(sentTop)
