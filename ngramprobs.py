## n-gram probabilities
import nltk
from collections import Counter
from nltk import SimpleGoodTuringProbDist, FreqDist
from indices import parse



def ngrams(filelist):
    uniwords=[]
    for f in filelist:
        uniwords.extend(parse(f))
    #create bi-,tri-,quadragram lists
    biwords=[]
    triwords=[]
    quadwords=[]
    words2=uniwords[1:]
    words3=uniwords[2:]
    words4=uniwords[3:]
    biwords=[uniwords[i] + ' ' + words2[i] for i in range(len(words2))]
    triwords=[uniwords[i] + ' '  + words2[i] + ' '  + words3[i] for i in range(len(words3))]
    quadwords=[uniwords[i] + ' '  + words2[i] + ' '  + words3[i] + ' '  + words4[i] for i in range(len(words4))]
    return (uniwords, biwords, triwords, quadwords)

def ngramcounts(uniwords, biwords, triwords, quadwords):
    #initialize word count dictionaries
    unicount=Counter(uniwords)
    bicount=Counter(biwords)
    tricount=Counter(triwords)
    quadcount=Counter(quadwords)    
    return (unicount, bicount, tricount, quadcount)

def GTprobs(unicount, bicount, tricount, quadcount):
    #NLTK Simple GT Probs
    uniGT=SimpleGoodTuringProbDist(FreqDist(unicount))
    biGT=SimpleGoodTuringProbDist(FreqDist(bicount))
    triGT=SimpleGoodTuringProbDist(FreqDist(tricount))
    quadGT=SimpleGoodTuringProbDist(FreqDist(quadcount))
    return (uniGT, biGT, triGT, quadGT)


