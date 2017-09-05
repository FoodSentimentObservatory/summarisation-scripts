import xlwt
import csv
import json
#function to generate a spreadsheet of the topic summaries
from configparser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config.txt')

path = parser.get('[folder-paths]', 'results')
def summarySpreadsheet(rows):
	wb = xlwt.Workbook()
	wordFormat = xlwt.easyxf('align: wrap yes, horiz centre; font: name Calibri, height 220; border: left thin, top thin, right thin')
	sheet1 = wb.add_sheet('Sheet 1')
	i = 1
	r=0
	xlwt.add_palette_colour("custom_colour", 0x21)
	wb.set_colour_RGB(0x21, 237, 125, 49)

	xlwt.add_palette_colour("pale_orange", 0x23)
	wb.set_colour_RGB(0x23, 252, 228, 214)
	#setting up formats for the cells
	sidestyle = xlwt.easyxf('pattern: pattern solid, fore_colour custom_colour; align: horiz centre; font: name Calibri, height 220, bold on; border: left medium, top medium, right medium')
	summStyle = xlwt.easyxf('pattern: pattern solid, fore_colour custom_colour; align: vert centre; font: name Calibri, height 220, bold on;border: left medium, top medium, right medium ')
	emptyLine = xlwt.easyxf('pattern: pattern solid, fore_colour pale_orange;')
	#function to generate header cells
	summaryHeaders(r, sheet1, sidestyle, summStyle,emptyLine)
	#going through each summary
	for row in rows:
		#setting up the dimentions of the cells
		sheet1.col(i).width = 12800
		sheet1.row(r).height_mismatch = True
		sheet1.row(r).height = 240*2
		#populating the cells with data, format: row, col, data, format 
		sheet1.write( r,i,row[0], sidestyle)
		sheet1.write( r+1, i,row[1], wordFormat)
		sheet1.write(r+2,i,row[2], wordFormat)
		sheet1.write(r+3,i,row[5], wordFormat)
		sheet1.write(r+4,i, row[4], wordFormat)
		sheet1.write(r+5,i," ",emptyLine )
		sheet1.write(r+6,i," ",emptyLine )
		i+=1
		#splitting the summaries to 5 per level
		if i%5==1 and i!=46:			
			r+=7
			i=1
			summaryHeaders(r, sheet1,sidestyle,summStyle, emptyLine)

	wb.save('./%s/summaries.xls' %(path))
	print ("Spreadsheet ready!")
#function to generate header cells
def summaryHeaders(r, sheet1, sidestyle,summStyle, emptyLine ):
	
	sheet1.col(0).width = 4000
	sheet1.write(r,0,'topic label', sidestyle)
	sheet1.write(r+1,0,'topic words', sidestyle)
	sheet1.write(r+2,0, 'topic importance', sidestyle)
	sheet1.write(r+3, 0, 'sentiment', sidestyle)
	sheet1.write(r+4, 0, 'Topic summaries', summStyle)	
	sheet1.write(r+5,0," ",emptyLine )
	sheet1.write(r+6,0," ",emptyLine )

def topicWordsSpreadsheet(topics):	
	wb = xlwt.Workbook()
	sheet1 = wb.add_sheet('Sheet 1')
	i = 1
	r=0

	xlwt.add_palette_colour("custom_colour", 0x21)
	wb.set_colour_RGB(0x21, 237, 125, 49)

	xlwt.add_palette_colour("pale_orange", 0x23)
	wb.set_colour_RGB(0x23, 252, 228, 214)

	sidestyle = xlwt.easyxf('pattern: pattern solid, fore_colour custom_colour; align: horiz centre; font: name Calibri, height 220, bold on; border: left medium, top medium, right medium, bottom medium')
	wordFormat = xlwt.easyxf('align: wrap yes, horiz centre; font: name Calibri, height 220; border: left thin, top thin, right thin, bottom thin')
	topicHeaders(r,sheet1, sidestyle)
	for topic in topics:
		words = topic[1]
		sheet1.col(i).width = 8000
		sheet1.write( r,i,topic[0], sidestyle)
		n=r+1
		for word in words:
			sheet1.write( n, i,word, wordFormat)
			n+=1		
		i +=1

		if i%15==1:
			r+=23
			i = 1
			topicHeaders(r,sheet1, sidestyle)

	wb.save('./%s/topics.xls' %(path))
	print ("Spreadsheet ready!")		

def topicHeaders(r,sheet1, sidestyle):
	sheet1.write(r,0,'topic label', sidestyle)
	i = r+1
	for i in range(i,r+21):
		sheet1.write(i,0,'word'+str(i), sidestyle)

def writeCsvFile(tupleList):

    with open('./%s/topicWords.csv' %(path),'w',newline='', encoding = 'utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(tupleList)

    print ("A csv file of topic words has been created has been generated.")		

def genJson(jsonRows):
		dic = {}
		dic['keyword']=''
		dic['location']=''
		dic['topics']=[]
	
		for row in jsonRows:
			topic={}
			topic['topicWords']=row[1]
			topic['topicSummaries']=row[3]
			topic['probability']=row[2]
			topic['sentiment']=row[4]

			dic['topics'].append(topic)
		#for row in jsonRows:
		jsonFormat =  json.dumps(dic)	
		
		#for top in topics:
		with open('./%s/jsonFile.json' %(path),'w', encoding='utf=8') as f:
			f.write(jsonFormat)
			



