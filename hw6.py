# -*- coding: utf-8 -*-
"""
Created on Sun March 5 03:24:06 2014

@author: haotianhe

LING 571 HW 6

Word Sense Disambiguation
"""

import sys
import itertools

from nltk.corpus import wordnet,wordnet_ic
from nltk import wordpunct_tokenize
from nltk.corpus.reader.wordnet import information_content

def removeBrackets(variable):
    return str(variable).replace('[','').replace(']','')

def removeQuotes(variable):
    return str(variable).replace('\'','').replace('\'','')

def similarityFunction(prob, word):
	firstTime = 1
	value = 0.0
	probTraverse = wordnet.synsets(prob, pos=wordnet.NOUN)
	wordTraverse = wordnet.synsets(word, pos=wordnet.NOUN)
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
	return dictionary



if __name__ == "__main__":

	wnic = wordnet_ic.ic('ic-brown-resnik-add1.dat')
	wsd_contexts = sys.argv[1]
	sents = open(wsd_contexts, 'r')

	for line in sents:
		WSD = wordpunct_tokenize(line)
		temp = []
		misDictionary = {}
		for word in WSD:
			if word is not ',':
				temp.append(word)
		result = []
		dictionary = {}
		for i in range(len(temp)):
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
		print str(', '.join(result).replace('),', ')')) + '\n'
		print str(max(misDictionary, key=misDictionary.get)) + '\n'
