import sys
import os
from operator import itemgetter
from itertools import groupby
import re
import docParsingFunctions
#function to map the topic values to sentiments

#main function
def topicOfDocument():
	listOfTopTopics = []
	topTopics = docParsingFunctions.mainTopics()
	topSents = docParsingFunctions.mainSentiment()
#call the mainSentiment and mainTopics function in order to populate those lists
	
	overalTopicValues = []
	#looping through each topic
	for topic in topTopics:
		topicLabel = topic[2][0]
		#print (topicLabel)
		docIndex = topic[0][1]
		docIndexList = [item for sublist in docIndex for item in sublist]
		docIndexStr = ''.join(docIndexList)
		sentimentLabel = topic[1]
		#for each topic we loop through each sentiment in order to find any corresponding values based on the document indexes
		for sent in topSents:
			for sentiment in sent:
				if docIndex == sentiment[0] and sentimentLabel == sentiment[2]:
					topicValue = topic[2][1][1]
					#once there's a match, the real topic probability is calculated by multiplying the sentiment probability of the topic
					#and the topic probability for that sentiment; those values are then saved
					overalValue = float(sentiment[3])*float(topicValue)
					tup = (docIndexStr,topic, overalValue)
					overalTopicValues.append(tup)
	listOfTopDocuments(overalTopicValues, listOfTopTopics)
	return listOfTopTopics	

def listOfTopDocuments(overalTopicValues, listOfTopTopics):					
	#the values are grouped by document and for each document the highest value is selected
	dic = {}
	f = lambda x: x[0]
	for key, group in groupby(sorted(overalTopicValues, key=f), f):
		dic[key] = list(group)	
			
	for key, value in dic.items():
		sortedTopics = sorted(value, key=itemgetter(2), reverse = True)
		topicOfDoc = sortedTopics[0]
		listOfTopTopics.append(topicOfDoc)

	

	
	


				

