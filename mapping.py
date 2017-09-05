import os
import sys
import re
import config
#opening a pi file and extracting the doc index and making them match the file name format
def readFile(files):
	fileNames = []
	documentPiFile = config.getDocumentPi()
	with open (documentPiFile, "r") as doc:
		lines = [line.split() for line in doc.readlines()]
		
		for line in lines:
			fileNameData = []
			for word in line:
				if "d_" in str(word):
					fileNameData.append(word)
			fileNames.append(fileNameData)	

	for couple in fileNames:
		docName = couple[1]	
		fileName  = re.sub(r'[<d_>\s]', '', str(docName))
		docIndex = couple[0]
		fileIndex = re.sub(r'd_','', str(docIndex))
		fileTuple = (fileIndex, fileName)
		files.append(fileTuple)
#mapping those doc indexes to their corresponding filenames in the raw tweets		
rawFiles = []
def mapToRawFiles():
	path =  config.rawTweetsPath()
	files = []
	readFile(files)	

	for tup in files:
		fileNameStr = tup[1]+"_texts_"
		for root, dir_names, file_names in os.walk(path):
			for path in dir_names:
				read_files(os.path.join(root, path))
			for file_name in file_names:
				if str(fileNameStr) in str(file_name):
					file_path = os.path.join(root, file_name)
					if os.path.isfile(file_path):
						past_header, lines = False, []
						f = open(file_path, 'r',errors='ignore')
						
						for line in f:                    
								lines.append(line)
						f.close()
					rawFileTuple = (tup[0],fileNameStr, lines)	
					rawFiles.append(rawFileTuple)			

mapToRawFiles()	