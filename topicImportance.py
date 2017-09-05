import sys
import os
from itertools import groupby
import docParsingFunctions

def topicOfDocument():
	topTopics =  docParsingFunctions.mainTopics()
	topSents = docParsingFunctions.mainSentiment()
#call the mainSentiment and mainTopics function in order to populate those lists
	dataForFile = []
	overalTopicValues = []
	#loops through each sentiment for each document and tries to map it to corresponding topics
	for sent in topSents:
		for sentiment in sent:
			for top in topTopics:
				docIndex = top[0][1]				
				sentimentLabel = top[1]	
				#if the document indexes and sentiment indexes match, there is a...match
				if docIndex == sentiment[0] and sentimentLabel == sentiment[2]:
							topicValueList = top[2]
							#lopps through the matched topic
							for val in topicValueList:
								topicLabel = val[0]
								prob = val[1]
#overal importance of the topic for the given document calculated by multiplying the sentiment value for that.. 
#..document with the probability of that topic within that sentiment
#Note: Each topic baring a sentiment has a thetha value and all thetha values for a sentiment for a document sum up to 1.00, 
#however, the real importance of a topic for a doc is calculated by multiplying that thetha by the value of the sentiment.. 
#..for that topic for that doc hence sometimes the main topic of a doc isn't always the one with the highest thetha.
								overalValue = float(sentiment[3])*float(prob)
#saving topic label, doc indexes, overal importance for that document, sentiment label, sentiment value, thetha				
								topicProb = (topicLabel, docIndex, overalValue, sentiment[2], sentiment[3], prob)
								overalTopicValues.append(topicProb)
	overalTopicCalculation(overalTopicValues, dataForFile)
	return dataForFile	


def overalTopicCalculation(overalTopicValues,dataForFile):								
	#grouping the topic values by topic label
	dic = {}
	f = lambda x: x[0]
	for key, group in groupby(sorted(overalTopicValues, key=f), f):
		dic[key] = list(group)	
	#for each topic label, calculate the sum of overal topic values across the corpus
	#and add to a list the topic label, sentiment and overal importance
	for key, value in dic.items():
		valueList = []
		sentiment = ""
		docValue = []
		for topicProb in value:
			prob = topicProb[2]
			probStr = str(prob)
			valueList.append(prob)
			sentiment = topicProb[3]
			documentName = "Document "+topicProb[1]
			docValue.append(documentName)
		
		topicValue = sum(valueList)
		topicData = (key,sentiment, topicValue)

		dataForFile.append(topicData)
			
	
