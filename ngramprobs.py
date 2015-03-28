## n-gram probabilities
import re
import math
import nltk
from collections import Counter
from nltk import SimpleGoodTuringProbDist
from nltk import pos_tag

def parse(filename):
    f=open('C:/Users/Betty/Documents/Homework/Comp/final project/greenEggs.txt')
    #f=open(filename)
    uniwords=[]
    for line in f:
        line.lower()
        re.sub("[^a-zA-Z!\.]", " ", line)#strip punctuation
        re.sub("(.|!)", " <s> <\s> ", line) #change . or ! to sentence boundary markers #DEBUG
        #lowercase
        splitwords=line.split()
        uniwords.append(splitwords)
        #delimit words by space.  
    return uniwords[0]

def ngramprobs(filename):
    uniwords=parse(filename)
    #create bi-,tri-,quadragram lists
    biwords=[]
    triwords=[]
    quadwords=[]
    words2=uniwords[1:]
    words3=uniwords[2:]
    words4=uniwords[3:]
    biwords=[uniwords[i] + words2[i] for i in range(len(words2))]
    triwords=[uniwords[i] + words2[i] + words3[i] for i in range(len(words3))]
    quadwords=[uniwords[i] + words2[i] + words3[i] + words4[i] for i in range(len(words4))]

    #initialize word count dictionaries
    unicount=Counter(uniwords)
    bicount=Counter(biwords)
    tricount=Counter(triwords)
    quadcount=Counter(quadwords)

##    #unigram good-turing probabilities
##    n=len(words)
##    univalues=dict(unicount).values() #counts from word count dicts
##    uniN=Counter(univalues) # Frequency of Frequencies
##    uniGTProbs=[uniN[1]/float(n)]  # Unseen probability mass
##    uniGTProbs.append([(float(i+1)*uniN[i+1]/uniN[i])/n for i in range(len(uniN)-1)])
##    #smoothing goes here

    #NLTK Simple GT Probs
    uniGT=SimpleGoodTuringProbDist(unicount)
    biGT=SimpleGoodTuringProbDist(bicount)
    triGT=SimpleGoodTuringProbDist(tricount)
    quadGT=SimpleGoodTuringProbDist(quadcount)
    return (uniGT, biGT, triGT, quadGT)

def wordlengthSD(filename):
    uniwords=parse(filename)
    #word length distributions
    #later include extra step to remove punctuation
    wordlengths=[len(uniwords[i]) for i in range(len(uniwords))]
    #calculate standard deviation
    avg=float(sum(wordlengths))/len(wordlengths)
    sumsq=sum([(avg-wordlengths[i])**2 for i in range(len(wordlengths))])
    return math.sqrt(sumsq/(len(wordlengths)-1))

def bagofwords(filename, numResults):
    uniwords=parse(filename)
    # bag of words (POS and raw words)
    tagged=nltk.pos_tag(uniwords)
    unicount=Counter(uniwords)
    taggedcount=Counter(tagged)
    wordbag=unicount.most_common()[:n-1]
    POSbag=taggedcount.most_common()[:n-1]
    return (wordbag, POSbag)
