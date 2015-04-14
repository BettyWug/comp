import math, nltk, random, re #numpy
from collections import Counter
from nltk import SimpleGoodTuringProbDist, FreqDist
from nltk import pos_tag
#from ngramprobs import ngrams, ngramcounts, GTprobs



### Input: a string
### Author: Nick
### Reviewed: 
### Output: the same string, but tokenized into a list using the
###  word_tokenize() function from nltk
### Comments:
###  -Gets input ready for nltk functions
###  -Also used to clean data when punctuation is irrelevant
def tokenize(s):
	s = list(s)
	for i, c in enumerate(s):
		val = (not c.isalnum() and not c.isspace()) or c == '\n'
		if val:
			s[i] = ' '
	s = ''.join(s)
	output = nltk.word_tokenize(s)
	return output

### Author: Betty
### Reviewed: 
### Input: a filename
### Output: ttokenised list with sentence boundary markers
###  word_tokenize() function from nltk
### Comments:
###  -like tokenize, except when punctuation is relevant
def parse(line):
    #f=open(filename)
    uniwords=['<s>']
    line.lower()
    nopunct=re.sub("[^a-zA-Z?!.]", " ", line)#strip punctuation, except ?!.
    delimited=re.sub("(\.|\!|\?)", " <\s> <s> ", nopunct) #change .?! to sentence boundary markers #DEBUG
    splitwords=delimited.split()
    uniwords.extend(splitwords)
    uniwords.extend(['<\s>'])
    return uniwords

### Author: Nick
### Reviewed: 
### Input: a string
### Output: a list of the sentence lengths in that string
### Comments:
###  -Should contractions be one or two words? Here, they're two
###  -Also, numerals are currently basically treated as punctuation
###  -Can't handle characters like accents--might be a problem if we
###   want to do foreign languages. Could easily be coded in though.
###  -Weird problem w/ Huck Finn
def getSenLens(input):
	senLens = []
	counter = 0
	for i, c in enumerate(input):
		if not type(c) is str:
			return senLens
		if not c.isalpha() or i+1 == len(input):
			if input[i-1].isalpha():
				counter += 1
		if c in ['!','.','?'] or i+1 == len(input):
			senLens.append(counter)
			counter = 0
	return senLens

### Author: Nick
### Reviewed: 
### Input: a string
### Output: a list of word lengths in that string
###
def getWordLens(input):
	wordLens = []
	words = tokenize(input)
	for w in words:
		wordLens.append(len(w))
	return wordLens

### Author: Nick
### Reviewed: 
### Input: a string
### Output: A dictionary of unigram counts over that string
### Comments:
###  -Does this deal with capitalization correctly?
def getUniCounts(input):
	words = tokenize(input)
	counts = dict()
	for w in words:
		if w not in counts:
			counts[w] = 1
		else:
			counts[w] += 1
	return counts


### END OF HELPER FUNCTIONS

### Author: Nick
### Reviewed: Betty (removed numpy)
### Input: a string
### Output: average sentence length over that string
### Comments:
###  -See getSenLens()
def aveSenLen(input):
	if len(input) == 0:
		return 0
	senLens = getSenLens(input)
	return sum(senLens)/float(len(senLens))

### Author: Nick
### Reviewed: Betty (removed numpy, divide by 0 error)
### Input: a string
### Output: standard deviation of sentence length over that string
### Comments:
###  -See getSenLens()
def senLenVar(input):
	if len(input) == 0:
		return 0
	senLens = getSenLens(input)
	if len(senLens) >= 1:
		return 0
	#std = numpy.std(senLens)
	avg=float(sum(senLens))/len(senLens)
	sumsq=sum([(avg-senLens[i])**2 for i in range(len(senLens))])
	std = math.sqrt(sumsq/(len(senLens)-1))
	return std

### Author: Nick
### Reviewed: Betty (removed numpy)
### Input: a string
### Output: average word length over that string
### Comments:
###  -Basically the same as for getSenLens()
def aveWordLen(input):
	wordLens = getWordLens(input)
	if len(wordLens) == 0:
		return 0
	return sum(wordLens)/float(len(wordLens))

### Author: Nick
### Reviewed: 
### Input: a string
### Output: a dictionary with proportions of each POS in the input
### Comments:
###  -Careful, very slow
###  -There is no entry in the dictionary for POS's unattested in
###    the input
###  -Betty: script relies on numpy
def getPosDist(input):
	words = tokenize(input)
	output = dict()
	pos = nltk.pos_tag(words)
	for pair in pos:
		for t in ['CC','CD','DT','EX','FW','IN','JJ','JJR','JJS','LS','MD','NN','NNS','NNP','NNPS','PDT','POS','PRP','PRP$','RB','RBR','RBS','RP','SYM','TO','UH','VB','VBD','VBG','VBN','VBP','VBZ','WDT','WP','WP$','WRB']:
			output[t] = 0
		if pair[1] not in output:
			output[pair[1]] = 1
		else:
			output[pair[1]] += 1
	total = sum(output.values())
	for t in output:
		output[t] /= total
	return output

### Author: Nick
### Reviewed: 
### Input: a string, a sample size
### Output: Average type-to-token ratio over a sample size of n
###  tokens in the input string
### Comments:
###  -It's sensitive to n so that the output is more relevant to the
###    specific length of the input
def getAveTTR(input, n):
	text = tokenize(input)
	random.shuffle(text)
	if n > len(text):
		print 'ERROR: n TOO LARGE'
		return -1
	ttrs = []
	for x in range(len(text)):
		if x+n < len(text):
			temp = text[x:x+n]
		else:
			temp = text[x:] + text[:n-(len(text)-x)]
		counts = dict()
		for w in temp:
			if w in counts:
				counts[w] += 1
			else:
				counts[w] = 1
		counts = counts.values()
		tokenCount = sum(counts)
		typeCount = len(counts)
		ttr = float(typeCount)/float(tokenCount)
		ttrs.append(ttr)
	return sum(ttrs)/float(len(ttrs))

### Author: Nick
### Reviewed: 
### Input: a string, and a dictionary of unigram counts
### Output: perplexity of the string under the language model
###  defined by using the smoothing method from midterm of the counts
###  in the input dictionary
### Comments:
###  -Can take dictionary input from getUniCounts()
###  -Maybe prep stuff (e.g., missing mass calculation, generation of
###    probability dictionary, etc.) can be combined w/ getUniCounts()?
def getUniPerp(s, counts):
	### Calculates 'missing mass' probability
	n = 0
	for x in counts.values():
		n += x
	n1 = 0
	for w in counts:
		if counts[w] == 1:
			n1 += 1
	mProb = float(n1)/float(n)
	### Generates probability dictionary using no. of incidences
	###  as keys (e.g., if counts['foo'] = 5, probs[5] represents
	###  smoothed unigram probability of 'foo')
	nCounts = dict()
	highest = 0
	for w in counts:
		if counts[w] in nCounts:
			nCounts[counts[w]] += 1
		else:
			nCounts[counts[w]] = 1
		if counts[w] > highest:
			highest = counts[w]
	for i in range(highest+1):
		if 1<i<6:
			if not i+1 in nCounts:
				nCounts[i+1] = 0
			nCounts[i] = float(nCounts[i+1])/float(nCounts[i])
			nCounts[i] *= nCounts[i+1]
	probs = dict()
	for x in nCounts:
		probs[x] = nCounts[i]/n
	### Actually calculates perplexity
	pp = float(0)
	text = tokenize(s)
	for w in text:
		if w in nCounts:
			pp *= math.log10(probs[nCounts[w]])
		else:
			pp += math.log10(mProb)
	pp *= (-1/float(n))
	pp = math.pow(10, pp)
	return pp

### Author: Betty
### Reviewed: 
### Input: a string
### Output: sd of word lengths
### Comments:
###  -
def wordlengthSD(s):
    uniwords=tokenize(s)
    #list of word lengths
    wordlengths=[len(uniwords[i]) for i in range(len(uniwords))]
    if len(wordlengths) <=1:
            return 0    
    #calculate standard deviation
    avg=float(sum(wordlengths))/len(wordlengths)
    sumsq=sum([(avg-wordlengths[i])**2 for i in range(len(wordlengths))])
    return math.sqrt(sumsq/(len(wordlengths)-1))

### Author: Betty
### Reviewed: 
### Input: a string, return n number of top results
### Output: n most common words (and POS tags)
### Comments:
###  -POS tags require numpy
def bagofwords(s, numResults):

    # bag of words (POS and raw words)
    uniwords=tokenize(s)
    #tagged=nltk.pos_tag(uniwords)

    #count word tokens
    unicount=Counter(uniwords)
    # count tags
    #taggedcount=Counter(tagged)

    #find n most common
    if numResults > len(unicount):
            print 'Error: bagofwords parameter numResults is greater than number of types.  Choose smaller number next time.'
    wordbag=unicount.most_common()[:numResults]
    wordbag=dict(wordbag)
    #POSbag=taggedcount.most_common()[:numResults]
    
    return (wordbag.keys())#, POSbag)


### Author: Betty
### Reviewed: 
### Input: 
### Output: 
### Comments:
###  -Originally in ngramprobs.py, but moved here for simplicity
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


### Author: Betty
### Reviewed: 
### Input: filename, Good-Turing probabilities of ngrams from an author (output of GTprobs)
### Output: returns uni-, bi-, tri-, quadra-gram log-probability of text in filename
### Comments:
###  -POS tags require numpy
def getngramprobs(filename, uniGT, biGT, triGT, quadGT):
        [unigrams, bigrams, trigrams, quadgrams]=ngrams([filename])
        uniprob=0
        biprob=0
        triprob=0
        quadprob=0
        flag=0
        for i in range(len(unigrams)):
                prob=uniGT.prob(unigrams[i])
                if prob< 0.00000001:
                        prob= 0.00000001
                        flag=1
                uniprob+=math.log10(prob)
        for i in range(len(bigrams)):
                prob=biGT.prob(bigrams[i])
                if prob< 0.00000001:
                        prob= 0.00000001
                        flag=1
                biprob+=math.log10(prob)
        for i in range(len(trigrams)):
                prob=triGT.prob(trigrams[i])
                if prob< 0.00000001:
                        prob= 0.00000001
                        flag=1
                triprob+=math.log10(prob)
        for i in range(len(quadgrams)):
                prob=quadGT.prob(quadgrams[i])
                if prob< 0.00000001:
                        prob= 0.00000001
                        flag=1
                quadprob+=math.log10(prob)
        if flag:
                print "SimpleGT error: unknown probability is 0.0. Smoothing applied."
        return (uniprob, biprob, triprob, quadprob)
