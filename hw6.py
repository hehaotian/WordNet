#!/usr/bin/env python2.5
# Park, Jonggun
# Professor Levow
# TA: Glenn Slayden
# Ling 571
import itertools
from nltk.corpus import wordnet,wordnet_ic
from nltk import wordpunct_tokenize                     #Tokenize
import sys
from nltk.corpus.reader.wordnet import information_content
output = "result"
outputPrint = open(output, 'w')
wnic = wordnet_ic.ic('ic-brown-resnik-add1.dat')
wsd_contexts = sys.argv[1]
Examples = open(wsd_contexts, 'r')                    # Example sentences.

def removeBrackets(variable):
    return str(variable).replace('[','').replace(']','')

def removeQuotes(variable):
    return str(variable).replace('\'','').replace('\'','')

def similarityFunction(prob, word):
	firstTime = 1
	value = 0.0
	# This part of the code will acquire all the synonyms of the Probe word and from theGiven words.
	probTraverse = wordnet.synsets(prob, pos=wordnet.NOUN)
	wordTraverse = wordnet.synsets(word, pos=wordnet.NOUN)
	# It traverses every single synonym from the prob word
	# comparing with all the synonyms of the given word
	# By having those values, the code gets all the
	# common hypernyms of those 2 synonyms.
	# it saves the highest information content and the MIS.
	for i in range(len(probTraverse)):
		for j in range(len(wordTraverse)):
			hypernyms = probTraverse[i].common_hypernyms(wordTraverse[j])
			for k in range(len(hypernyms)):
				if firstTime == 1:
					firstTime = 2
					name = hypernyms[k].name
					temp = wordnet.synset(name)
					value = information_content(temp, wnic)
					MIS = probTraverse[i].name # save this <-- MIS
					dictionary = {MIS : value}
				else:
					name2 = hypernyms[k].name 
					temp2 = wordnet.synset(name2)
					checkValue = information_content(temp2, wnic)	# save the new information content if it is higher
					if value <= checkValue:
						MIS = probTraverse[i].name
						dictionary = {MIS : checkValue}
	# It returns a dictionary which contains the MIS and the information content value.
	return dictionary

# Reads in the data.
# This part of the code, reads in the given data line by line and word by word.
for line in Examples:
	WSD = wordpunct_tokenize(line)
	temp = []
	misDictionary = {}
	for word in WSD:
		if word is not ',':
			temp.append(word)
	result = []
	dictionary = {}
	for i in range(len(temp)):			# if there are 2 words and 1 probe, we run it twice 
		if i > 0:
			hotline = removeBrackets(temp[2])
			hotline = str(hotline)
			if hotline != 'hotline':
				dictionary = similarityFunction(temp[0], temp[i]) 
				value = dictionary.values()
				temporary = str(dictionary.values())
				temporary = removeBrackets(temporary)
				newMIS = removeBrackets(dictionary.keys()) # = MIS
				newMIS = removeQuotes(newMIS)
				result.append("(" + temp[0] + ", " + temp[i] + ", " + temporary + ")")
				misDictionary.update({newMIS : value})
			else:
				result.append("(" + temp[0] + ", " + temp[i] + ", " + temporary + ")")
				misDictionary.update({newMIS : value})
	# At this point, we have found the highest sense given all the words.
	outputPrint.write(str(', '.join(result).replace('),', ')')) + '\n')
	outputPrint.write(str(max(misDictionary, key=misDictionary.get)) + '\n')
	#print newMIS

outputPrint.close()
