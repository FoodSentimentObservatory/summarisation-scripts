import sys
from itertools import groupby
from operator import itemgetter
import re
import docTopics
import collections
import csv
import topicImportance
import generateSpreadsheets
from configparser import SafeConfigParser
import similarityCheck

parser = SafeConfigParser()
parser.read('config.txt')

topTopics = topicImportance.topicOfDocument()
topTopicsOfDocs = docTopics.topicOfDocument()
#function to read txt files and create dictionaries split by topic both for sentences and for words
def readFile (doc, finalList, dic, fullList):
	
	lines = [line.split() for line in doc.readlines()]
	listOfWord = []
	topicLabel = " "
	for line in lines:
		wordList = []
		if "_Topic" in str(line):

			topicLabel = line
		else:
			wordList = [topicLabel, line]	
			topicWord = [item for sublist in wordList for item in sublist]
			finalList.append(topicWord)
		
	f = lambda x: x[0]
	for key, group in groupby(sorted(finalList, key=f), f):
		dic[key] = list(group)			

#calls the read function for topic words and generates a dictionary 
def readTopicWords(dicW) :
	fullList = []
	topicWordFile = parser.get('file-paths', 'topicWords')
	doc = open(topicWordFile, "r", encoding='utf-8')
	topicWords = []
	readFile(doc, topicWords, dicW, fullList)
	print("topics read")
#calls the read function for topic sentences and generates a dictionary	
def readTopicSentences(dicS):	
	fullList = []
	topicSentencesFile = parser.get('file-paths', 'topicSentences')
	doc = open (topicSentencesFile, "r", encoding='utf-8')
	topicSentences = []
	readFile(doc, topicSentences, dicS, fullList)
	print ("sentences read")
#function to creat lists of topic words
def sortTopicWords(topics, dicW):
	spreadsheetTopics=[]
	topicsAndProbs = []
	for key, value in dicW.items():
		textAndProbs = []
		text = []
		wordTopicID = key
		textAndProbs.append(key)
		for topic in value:
			
			for word in topic:
				
				if word.isalpha()==True:
					text.append(word)

		topicsAndProbs.append(textAndProbs)

		
		textStr = ', '.join(text)
		spreadsheetTopicTuple = (wordTopicID, textStr)			
		topicTuple = (wordTopicID, text)
		topics.append(topicTuple)
		spreadsheetTopics.append(spreadsheetTopicTuple)
	generateSpreadsheets.writeCsvFile(topicsAndProbs)	
	generateSpreadsheets.topicWordsSpreadsheet(topics)
#function to extract the top ten sentences for each topic
def topTenSentences(value, topicID):
	sentenceTexts = []
	countList = []
	for sentence in value:
			text = []
			fileName = " "
			fileLine = " "
			probability = " "

			for word in sentence:
				wordS = str(word)
				#saves only the sentences into a list
				if word.isalpha()== True:
					text.append(word)
				#the location of the sentence in format docIndex_lineIndex is split into two separate values: docIndex and lineIndex	
				elif "_" in str(word) and "_Topic" not in str(word):
					location = word.split("_")
					fileLoc = location[0]
					fileName = re.sub(r'\[','',str(fileLoc))
					fileLine = location[1]
				elif len(wordS)==9 and "." in str(word):
					#saves the probability value in a variable
					probability = re.sub(r'\]','',str(word))
			#clean up of retweets, if a text has already been added to the list, this sentence does not proceed any further
			#else the sentence is added to a list for further sorting
			#if text not in sentenceTexts:
			sentenceTexts.append(text)
			sentenceList = (topicID, fileName, fileLine, text, probability)
			countList.append(sentenceList)
		#all selected sentences are sorted by their probability and then only the top 10 proceed to the next step		
	sortedCountList = sorted(countList, key=itemgetter(4), reverse = True)
	topTen = sortedCountList[:30]
	return topTen

def summary(topicSummaries, topics) :
	dicW = {}
	dicS = {}
	readTopicWords(dicW)
	readTopicSentences(dicS)
	sortTopicWords(topics, dicW)	

	# goes 	through the topic sentences dictionary 
	for k, value in dicS.items():
		topicID = k
		countedTopTen = []
		topTen = topTenSentences(value, topicID)
		removedSimilars = similarityCheck.removeSimilars(topTen)
		#loop through each sentence of the top ten
		for tweet in removedSimilars:
			count = 0
			tweetProb = tweet [4]
			text = tweet[3]
			#search for the corresponding topic in topics
			for tup in topics:
				if tup[0]==tweet[0]:
					topicWords = tup[1]
					#count the repetion of topic words within each sentence
			countTuple = (tweet[0], tweet[1], tweet[2], text, tweetProb)
			countedTopTen.append(countTuple)
		sortedList = sorted(countedTopTen, key=itemgetter(4), reverse = True)
		#storing the top three sentences for each topic in a list
		for tup in topics:
			if tup[0]==topicID:
				for sent in sortedList:
					topicSummaries.append(sent)
					

def mapToRawTexts():
	import mapping
	topicSummaries = []
	topics = []
	rawTexts = mapping.rawFiles
	#call the summary function to do fetch the relevant results
	summary(topicSummaries, topics)
	
	allTopics = []
	#loops through each topic from the list containing topics and words
	for topic in topics:		
		twordsID = topic[0]
		topicwords = ', '.join(topic[1])
		topDocs = []
		#getting the sentiment value for each topic
		sentiment = sentimentOfTopic(twordsID, topTopics)
		#function results to be used for sorting topics by importance
		importance = topicImportance(twordsID,  topTopics)
		#getting all the documents where this topic had the highest probability score
		topDocuments(twordsID, topTopicsOfDocs, topDocs)

		count = len(topDocs)
		sentence = []
		#loops through each of the top sentences for each topic
		wordCount = 0
		for sum in topicSummaries:				
			topicID = sum[0]
			if topicID == twordsID:				
				findex = sum[1]
				lineIndex = sum[2]
				#loops through the raw data to find the location match for each of the top three sentences
				for text in rawTexts:
					rawfindex = text[0]			
					if findex == rawfindex:
						i =0
						raw = text[2]
						for line in raw:
							i +=1	
							if int(lineIndex)+2 == i and wordCount <100:
								lineList = line.split(" ")
								sentence.append(line)
								wordCount+=len(lineList)
				
		#creating a list for each topic containing the topic label, topic words, the documents where the topic is top topic, the count of
		#those documents and the the top three sentences in raw format						
		topicData = [topic[0], topicwords, topDocs, count, sentence, sentiment, importance]
		allTopics.append(topicData)
	#sorting the topic data by topic label	
	allTopicsSorted = sorted(allTopics, key=itemgetter(6), reverse = True)
	printAndWriteResults(allTopicsSorted)

#function to print results on the console and save them in a txt file
def printAndWriteResults(allTopicsSorted):	
	rows = []
	jsonRows = []
	with open('./results/summary.txt','w', encoding = 'utf-8') as f:
		f.write("The topics have been ordered by importance in the whole corpus starting from the most important.\n")
		f.write("--- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---\n")
		f.write(" \n")
		for t in allTopicsSorted:		
			sentences = t[4]
			sentencesStr = ''.join(sentences)
			print (t[0])
			print (t[1])
			print ("The sentiment of this topic is: "+t[5])
			print ("The overal importance of the topic across the whole corpus is: " + str(t[6]))

			f.write("%s\n"%(t[0]))
			f.write("Topic words: %s\n"%(t[1]))
			f.write("The sentiment of the topic is: %s\n"%(t[5]))
			f.write("The overal importance of the topic across the whole doc corpus is: %s\n"%(str(t[6])))

			if t[3] != 0:
				listOfDocsStr = ', '.join(t[2])
				print ("This is the top topic for the following documents: " + listOfDocsStr)
				f.write("This is the top topic for the following documents: %s\n"%(listOfDocsStr))
			else:
				print("No documents have this topic as their top one")
				f.write("No documents have this topic as their top one\n")

			print (" ")
			print (sentencesStr)
						
			f.write(" \n")
			f.write("Summary of the topic generated from top tweets for each topic: \n")
			f.write(" \n")
			f.write("%s\n"%(sentencesStr))
			f.write("-------------------------------------------------------------------------------------- \n")

			print("-------------------------------------------------------------------------------------- ")	
			row = (t[0], t[1],t[6], listOfDocsStr, sentencesStr, t[5])
			jsonRow = (t[0], t[1], t[6], sentencesStr, t[5])
			jsonRows.append(jsonRow)
			#rows.append(row)
	#function to generate a spreadsheet of the topic summarisations, ordered by importance		
	generateSpreadsheets.genJson(jsonRows)	
	generateSpreadsheets.summarySpreadsheet(rows)		
	print ("Results save to a text file.")		
		

#extracting the value for topic importance
def topicImportance(topicID,  topTopics):
	for topic in topTopics:
		labelID = topic[0]
		if topicID == labelID:
			importance = topic[2]
	return importance	
#extracting the value for topic sentiment
def sentimentOfTopic(topicID, topTopics):
	for topic in topTopics:
		if topicID==topic[0]:
			sentiment=topic[1]
	return sentiment					
#extracting the values for documents where the topic is the most important one
def topDocuments(topicID, topTopicsOfDocs, topDocs):
	#print (topicID)
	for topic in topTopicsOfDocs:

		if topicID==topic[1][2][0][0]:
			docName = topic[1][0]
			docNameStr = ' '.join(docName)

			topDocs.append(docNameStr)
	
mapToRawTexts()		

