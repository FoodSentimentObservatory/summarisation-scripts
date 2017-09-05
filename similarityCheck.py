from difflib import SequenceMatcher
import itertools
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def removeSimilars(topTen):
	removedSimilars = topTen
	for p1, p2 in itertools.combinations(topTen, 2):
		
		#similarity = fuzz.ratio(p1[4], p2[4])
		if len(p1[3])<2:
			for r in removedSimilars:
				if r == p1:
					removedSimilars.remove(r)
		elif len(p2[3])<2:
			for r in removedSimilars:
				if r == p2:
					removedSimilars.remove(r)	
		else:	
			similarity = similar(p1[3], p2[3])				
			if similarity ==True :

				selected = max(p1[4],p2[4])
				for r in removedSimilars:
					if selected==p1[4]:
						if r == p2:
							removedSimilars.remove(r)
					else:
						if r==p1:
							removedSimilars.remove(r)	
	
	return removedSimilars			

def similar(seq1, seq2):
	return SequenceMatcher(a=seq1, b=seq2).ratio() > 0.7 

def test():
	a = "banana shake"
	b = "I love a banana shake during summer"

	similarity = similar(a, b)

	print (similarity)

	