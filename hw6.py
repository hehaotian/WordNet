# -*- coding: utf-8 -*-
"""
Created on Sun March 5 03:24:06 2014
@author: haotianhe
LING 571 HW 6
Word Sense Disambiguation
"""

import sys
from nltk.corpus import wordnet
from nltk.corpus import wordnet_ic
from nltk.corpus.reader.wordnet import information_content

def report(context_pair, wnic):
    best_senses = []
    results = []

    for i in xrange(len(context_pair)):
        word = context_pair[i][0]
        
        normal_fact = 0.0
        scores = dict()

        for context in context_pair[i][1]:
            resnik = resnik_similarity(word, context, wnic)

            if resnik:
                mis = resnik[0]
                sim = resnik[1]
                item = "(" + word + ", " + context + ", " + str(sim) + ") "
                print item,
                normal_fact += sim

                for sense in wordnet.synsets(word):
                    if mis in sense.common_hypernyms(sense):
                        scores.update({sense:sim})

            else:
                item = "(" + word + ", " + context + ", " + "None) "
                print item,

        for score in scores:
            scores[score] = scores[score] / normal_fact

        print("\n" + max(scores.iterkeys(), key=lambda x: scores[x]).name)


def resnik_similarity(word, context, wnic):
    
    probe_senses = wordnet.synsets(word)
    context_senses = wordnet.synsets(context)

    if not context_senses:
        return None

    top_subs = set()

    for sense in probe_senses:
        for context in context_senses:
            common_hypernyms = sense.common_hypernyms(context)
            if common_hypernyms:
                mark1 = max(common_hypernyms, key=lambda x: information_content(x, wnic))
                mark2 = information_content(mark1, wnic)
                top_subs.add((mark1, mark2))

    mis = max(top_subs, key=lambda x: x[1])
    
    return mis

def load_wsd_contexts(wsd_contexts):
    
    context_pair = []

    for sense in open(wsd_contexts, 'r'):
        sense = sense.strip().split()
        word = sense[0]
        contexts = sense[1].split(',')
        context_pair.append((word, contexts))

    return context_pair


if __name__ == "__main__":

    if (len(sys.argv) >= 2):
        wsd_contexts = sys.argv[1]
        ic_file = sys.argv[2]
    else:
        wsd_contexts = "/dropbox/13-14/571/hw6/wsd_contexts.txt"
        ic_file = "ic-brown-resnik-add1.dat"

    wnic = wordnet_ic.ic(ic_file)
    context_pair = load_wsd_contexts(wsd_contexts)
    report(context_pair, wnic)
